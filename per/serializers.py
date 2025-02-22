from rest_framework import serializers
from django.contrib.auth.models import User

from api.models import Region
from api.serializers import (
    RegoCountrySerializer, UserNameSerializer
)
from .models import (
    Form,
    FormArea,
    FormComponent,
    FormQuestion,
    FormAnswer,
    FormData,
    NSPhase,
    WorkPlan,
    Overview,
    NiceDocument,
    AssessmentType
)


class IsFinalOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overview
        fields = ('id', 'is_finalized')


class FormAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormArea
        fields = '__all__'


class FormComponentSerializer(serializers.ModelSerializer):
    area = FormAreaSerializer()

    class Meta:
        model = FormComponent
        fields = ('area', 'title', 'component_num', 'component_letter', 'description', 'id')


class FormAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormAnswer
        fields = '__all__'


class FormQuestionSerializer(serializers.ModelSerializer):
    component = FormComponentSerializer()
    answers = FormAnswerSerializer(many=True)

    class Meta:
        model = FormQuestion
        fields = ('component', 'question', 'question_num', 'answers', 'is_epi', 'is_benchmark', 'description', 'id')


class ListFormSerializer(serializers.ModelSerializer):
    area = FormAreaSerializer()
    user = UserNameSerializer()
    overview = IsFinalOverviewSerializer()

    class Meta:
        model = Form
        fields = ('area', 'overview', 'updated_at', 'comment', 'user', 'id')


class FormStatSerializer(serializers.ModelSerializer):
    area = FormAreaSerializer()
    overview = IsFinalOverviewSerializer()

    class Meta:
        model = Form
        fields = ('area', 'overview', 'id',)


class ListFormDataSerializer(serializers.ModelSerializer):
    selected_answer = FormAnswerSerializer()

    class Meta:
        model = FormData
        fields = ('form', 'question_id', 'selected_answer', 'notes', 'id')


class FormDataWOFormSerializer(serializers.ModelSerializer):
    selected_answer = FormAnswerSerializer()

    class Meta:
        model = FormData
        fields = ('question_id', 'selected_answer', 'notes', 'id')


class ListFormWithDataSerializer(ListFormSerializer):
    form_data = FormDataWOFormSerializer(many=True)

    class Meta:
        model = Form
        fields = ('area', 'overview', 'form_data', 'updated_at', 'comment', 'user', 'id')


class ListNiceDocSerializer(serializers.ModelSerializer):
    country = RegoCountrySerializer()
    visibility_display = serializers.CharField(source='get_visibility_display', read_only=True)

    class Meta:
        model = NiceDocument
        fields = ('name', 'country', 'document', 'document_url', 'visibility', 'visibility_display')


class ShortFormSerializer(serializers.ModelSerializer):
    area = FormAreaSerializer()
    overview = IsFinalOverviewSerializer()

    class Meta:
        model = Form
        fields = ('area', 'overview', 'updated_at', 'id',)


class EngagedNSPercentageSerializer(serializers.ModelSerializer):
    country__count = serializers.IntegerField()
    forms_sent = serializers.IntegerField()

    class Meta:
        model = Region
        fields = ('id', 'country__count', 'forms_sent',)


class GlobalPreparednessSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField(max_length=10)
    question_id = serializers.CharField(max_length=20)

    class Meta:
        fields = ('id', 'code', 'question_id',)


class NSPhaseSerializer(serializers.ModelSerializer):
    phase_display = serializers.CharField(source='get_phase_display', read_only=True)

    class Meta:
        model = NSPhase
        fields = ('id', 'country', 'phase', 'phase_display', 'updated_at')


class PerMiniUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class WorkPlanSerializer(serializers.ModelSerializer):
    user = PerMiniUserSerializer()
    prioritization_display = serializers.CharField(source='get_prioritization_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = WorkPlan
        fields = '__all__'


class AssessmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentType
        fields = '__all__'


class OverviewSerializer(serializers.ModelSerializer):
    user = PerMiniUserSerializer()
    country = RegoCountrySerializer()
    type_of_assessment = AssessmentTypeSerializer()
    included_forms = serializers.CharField(source='get_included_forms', read_only=True)

    class Meta:
        model = Overview
        fields = '__all__'


class LatestCountryOverviewSerializer(serializers.ModelSerializer):
    type_of_assessment = AssessmentTypeSerializer()

    class Meta:
        model = Overview
        fields = ('id', 'country_id', 'assessment_number', 'date_of_assessment', 'type_of_assessment')
