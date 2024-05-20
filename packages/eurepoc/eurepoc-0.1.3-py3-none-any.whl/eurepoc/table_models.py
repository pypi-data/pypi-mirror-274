from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MainData(BaseModel):
    incident_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    added_to_db: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    operation_type: Optional[str] = None
    status: Optional[str] = None
    updated_at: Optional[datetime] = None
    number_attributions: Optional[int] = None
    number_political_responses: Optional[int] = None
    number_legal_responses: Optional[int] = None
    casualties: Optional[str] = None

    class Config:
        from_attributes = True


class InclusionCriteria(BaseModel):
    incident_id: int
    inclusion_criterion: Optional[str] = None
    inclusion_criterion_subcode: Optional[str] = None

    class Config:
        from_attributes = True


class SourceDisclosure(BaseModel):
    incident_id: int
    source_disclosure: Optional[str] = None

    class Config:
        from_attributes = True


class IncidentType(BaseModel):
    incident_id: int
    incident_type: Optional[str] = None

    class Config:
        from_attributes = True


class Receiver(BaseModel):
    receiver_id: str
    incident_id: int
    receiver_name: Optional[str] = None
    receiver_country: Optional[str] = None
    receiver_country_alpha_2_code: Optional[str] = None
    receiver_country_alpha_3_code: Optional[str] = None
    receiver_category: Optional[str] = None
    receiver_subcategory: Optional[str] = None
    receiver_regions: Optional[list] = None

    class Config:
        from_attributes = True


class Attributions(BaseModel):
    attribution_id: str
    incident_id: int
    settled_attribution: Optional[bool] = None
    attribution_date: Optional[str] = None
    attribution_updated_at: Optional[datetime] = None
    attribution_created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AttributionBases(BaseModel):
    attribution_id: str
    attribution_basis: Optional[str] = None

    class Config:
        from_attributes = True


class AttributionTypes(BaseModel):
    attribution_id: str
    attribution_type: Optional[str] = None
    attribution_subtype: Optional[str] = None

    class Config:
        from_attributes = True


class AttributionCountries(BaseModel):
    attribution_id: str
    attributing_country: Optional[str] = None

    class Config:
        from_attributes = True


class AttributionActors(BaseModel):
    attribution_id: str
    attributing_actor: Optional[str] = None

    class Config:
        from_attributes = True


class AttributionCompanies(BaseModel):
    attribution_id: str
    attributing_company: Optional[str] = None

    class Config:
        from_attributes = True


class AttributionLegalReferences(BaseModel):
    attribution_id: str
    attribution_legal_reference: Optional[str] = None
    attribution_legal_reference_subcode: Optional[str] = None

    class Config:
        from_attributes = True


class Initiators(BaseModel):
    initiator_id: str
    incident_id: int
    attribution_id: Optional[str] = None
    settled_initiator: Optional[bool] = None
    initiator_name: Optional[str] = None
    initiator_country: Optional[str] = None

    class Config:
        from_attributes = True


class InitiatorsCategories(BaseModel):
    initiator_id: str
    initiator_category: Optional[str] = None
    initiator_subcategory: Optional[str] = None

    class Config:
        from_attributes = True


class CyberConflictIssues(BaseModel):
    incident_id: int
    cyber_conflict_issue: Optional[str] = None

    class Config:
        from_attributes = True


class OfflineConflictIssues(BaseModel):
    incident_id: int
    offline_conflict_issue: Optional[str] = None
    offline_conflict_name: Optional[str] = None

    class Config:
        from_attributes = True


class OfflineConflictIntensities(BaseModel):
    incident_id: int
    offline_conflict_intensity: Optional[str] = None
    offline_conflict_intensity_subcode: Optional[str] = None

    class Config:
        from_attributes = True


class PoliticalResponses(BaseModel):
    political_response_id: str
    incident_id: int
    political_response_date: Optional[str] = None
    political_response_responding_country: Optional[str] = None
    political_response_responding_actor: Optional[str] = None

    class Config:
        from_attributes = True


class PoliticalResponseTypes(BaseModel):
    political_response_id: str
    incident_id: int
    political_response_type: Optional[str] = None
    political_response_subtype: Optional[str] = None

    class Config:
        from_attributes = True


class TechnicalCodings(BaseModel):
    incident_id: int
    zero_days: Optional[str] = None
    zero_days_subcode: Optional[str] = None
    has_disruption: Optional[bool] = None
    user_interaction: Optional[str] = None

    class Config:
        from_attributes = True


class CyberIntensity(BaseModel):
    incident_id: int
    disruption: Optional[str] = None
    hijacking: Optional[str] = None
    data_theft: Optional[str] = None
    physical_effects_spatial: Optional[str] = None
    physical_effects_temporal: Optional[str] = None
    target_multiplier: Optional[str] = None
    unweighted_intensity: Optional[int] = None
    weighted_intensity: Optional[int] = None

    class Config:
        from_attributes = True


class MitreInitialAccess(BaseModel):
    incident_id: int
    mitre_initial_access: Optional[str] = None

    class Config:
        from_attributes = True


class MitreImpact(BaseModel):
    incident_id: int
    mitre_impact: Optional[str] = None

    class Config:
        from_attributes = True


class ImpactIndicator(BaseModel):
    incident_id: int
    impact_indicator_score: Optional[int] = None
    impact_indicator_label: Optional[str] = None
    functional_impact: Optional[str] = None
    intelligence_impact: Optional[str] = None
    economic_impact: Optional[str] = None
    economic_impact_value: Optional[int] = None
    economic_impact_currency: Optional[str] = None
    affected_entities: Optional[str] = None
    affected_entities_value: Optional[int] = None
    affected_eu_countries: Optional[str] = None
    affected_eu_countries_value: Optional[int] = None
    affected_third_countries: Optional[str] = None
    affected_third_countries_value: Optional[int] = None

    class Config:
        from_attributes = True


class LegalCodings(BaseModel):
    incident_id: int
    state_responsibility_actor: Optional[str] = None
    evidence_for_sanctions_indicator: Optional[str] = None
    response_indicator: Optional[str] = None

    class Config:
        from_attributes = True


class ILBreachIndicator(BaseModel):
    incident_id: int
    il_breach_indicator: Optional[str] = None
    il_breach_indicator_subcode: Optional[str] = None

    class Config:
        from_attributes = True


class LegalResponses(BaseModel):
    legal_response_id: str
    incident_id: int
    legal_response_date: Optional[str] = None
    legal_response_responding_country: Optional[str] = None
    legal_response_responding_actor: Optional[str] = None

    class Config:
        from_attributes = True


class LegalResponseTypes(BaseModel):
    legal_response_id: str
    incident_id: int
    legal_response_type: Optional[str] = None
    legal_response_subtype: Optional[str] = None

    class Config:
        from_attributes = True


class SourceUrls(BaseModel):
    source_urls_id: str
    incident_id: int
    source_url: Optional[str] = None

    class Config:
        from_attributes = True


class SourceNames(BaseModel):
    source_url_id: str
    incident_id: int
    source_name: Optional[str] = None

    class Config:
        from_attributes = True


class SourceCategories(BaseModel):
    source_url_id: str
    incident_id: int
    source_category: Optional[str] = None

    class Config:
        from_attributes = True


class AttributionSources(BaseModel):
    incident_id: int
    attribution_source_url: Optional[str] = None

    class Config:
        from_attributes = True


class Articles(BaseModel):
    article_id: int
    incident_id: int
    article_title: Optional[str] = None
    article_date: Optional[datetime] = None
    article_url: Optional[str] = None
    article_status: Optional[str] = None
    source_url: Optional[str] = None
    source_name: Optional[str] = None
    source_category: Optional[str] = None
    source_status: Optional[str] = None
    source_country: Optional[str] = None
    article_text: Optional[str] = None

    class Config:
        from_attributes = True


class Logs(BaseModel):
    log_id: int
    incident_id: int
    log_comment: Optional[str] = None
    log_date: Optional[str] = None

    class Config:
        from_attributes = True
