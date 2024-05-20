import requests as req
from nested_query_string import NestedQueryString


BASE_URL = "https://strapi.eurepoc.eu/api/incidents"
HEADERS = {
    'content-type': 'application/json'
}


def build_filters(
        flag_type=None, flag_status=None, receiver_region=None, receiver_country=None, date_type=None,
        range_start_date=None, range_end_date=None, status_conditions=None, receiver_category=None,
        initiator_country=None
):
    filters = []

    if flag_type and flag_status:
        filters.append(f"filters[{flag_type}]={flag_status}")

    if receiver_region:
        filters.append(f"filters[$and][][receiver][country][country_regions][region][name][$eq]={receiver_region}")

    if receiver_country:
        filters.append(f"filters[$and][][receiver][country][name][$eq]={receiver_country}")

    if date_type and range_start_date:
        filters.append(f"filters[{date_type}][$gte]={range_start_date}T00:00:00.000Z")

    if date_type and range_end_date:
        filters.append(f"filters[{date_type}][$lte]={range_end_date}T23:59:59.000Z")

    if status_conditions:
        status_filter = f"filters[$or][0][{status_conditions[0][0]}][$eq]={status_conditions[0][1]}&filters[$or][1][{status_conditions[1][0]}][$eq]={status_conditions[1][1]}"
        filters.append(status_filter)

    if receiver_category:
        filters.append(f"filters[$and][][receiver][category][code][title][$eq]={receiver_category}")

    if initiator_country:
        filters.append(f"filters[$and][][attributions][initiators][countries][name][$contains]={initiator_country}")

    return '&'.join(filters)


def build_query(
        flag_type=None, flag_status=None, receiver_region=None, receiver_country=None, date_type=None,
        range_start_date=None, range_end_date=None, status_conditions=None, receiver_category=None,
        initiator_country=None
):
    filters = build_filters(
        flag_type=flag_type, flag_status=flag_status, receiver_region=receiver_region, receiver_country=receiver_country,
        date_type=date_type, range_start_date=range_start_date, range_end_date=range_end_date,
        status_conditions=status_conditions, receiver_category=receiver_category,
        initiator_country=initiator_country
    )
    nested_query = NestedQueryString.encode({
        "sort": ["id:asc"],
        "populate": [
            "start",
            "end",

            "sources_attribution",
            "receiver",
            "receiver.category.code",
            "receiver.category.subcode",
            "receiver.country",
            "receiver.country.country_regions",
            "receiver.country.country_regions.region",

            "attributions",
            "attributions.articles",
            "attributions.initiators.countries",
            "attributions.initiators.category.code",
            "attributions.initiators.category.subcode",
            "attributions.countries_of_origin",
            "attributions.attribution_basis.code",
            "attributions.attribution_basis.subcode",
            "attributions.attribution_type.code",
            "attributions.attribution_type.subcode",
            "attributions.temporal_attribution_sequence.code",
            "attributions.temporal_attribution_sequence.subcode",
            "attributions.attribution_date",
            "attributions.attributing_actors",
            "attributions.attributing_country",
            "attributions.it_companies",
            "attributions.legal_attribution_references.code",
            "attributions.legal_attribution_references.subcode",

            "temporal_attribution_sequence.code",
            "temporal_attribution_sequence.subcode",

            "attributes",
            "attributes.incident_type.code",
            "attributes.incident_type.subcode",
            "attributes.data_theft.code",
            "attributes.data_theft.subcode",
            "attributes.zero_days_used.code",
            "attributes.zero_days_used.subcode",
            "attributes.hijacking.code",
            "attributes.hijacking.subcode",
            "attributes.disruption.code",
            "attributes.disruption.subcode",
            "attributes.weighted_cyber_intensity.code",
            "attributes.weighted_cyber_intensity.subcode",
            "attributes.target_effect_multiplier.code",
            "attributes.target_effect_multiplier.subcode",
            "attributes.casualities.code",
            "attributes.casualities.subcode",
            "attributes.physical_effects_spatial.code",
            "attributes.physical_effects_spatial.subcode",
            "attributes.physical_effects_temporal.code",
            "attributes.physical_effects_temporal.subcode",
            "attributes.offline_conflict_intensity.code",
            "attributes.offline_conflict_intensity.subcode",
            "attributes.cyber_conflict_issue.code",
            "attributes.cyber_conflict_issue.subcode",
            "attributes.offline_conflict_issue.code",
            "attributes.offline_conflict_issue.subcode",

            "inclusion_criteria.code",
            "inclusion_criteria.subcode",
            "source_incident_detection_disclosure.code",
            "source_incident_detection_disclosure.subcode",

            "legal_response",
            "political_response",

            "legal_response.date",
            "political_response.date",
            "legal_response.countries",
            "political_response.countries",
            "legal_response.actors",
            "political_response.actors",
            "legal_response.type.code",
            "legal_response.type.subcode",
            "political_response.type.code",
            "political_response.type.subcode",

            "evidence_for_sanctions",
            "evidence_for_sanctions.code",
            "evidence_for_sanctions.subcode",

            "response_indicator",
            "response_indicator.code",
            "response_indicator.subcode",

            "il_breach_indicator",
            "il_breach_indicator.code",
            "il_breach_indicator.subcode",

            "state_responsibility_indicator.code",
            "state_responsibility_indicator.subcode",

            "user_interaction.code",
            "user_interaction.subcode",

            "mitre_impact.code",
            "mitre_impact.subcode",

            "mitre_initial_access.code",
            "mitre_initial_access.subcode",

            "impact_indicator.economic_impact",
            "impact_indicator.economic_impact.code.code",
            "impact_indicator.economic_impact.code.subcode",
            "impact_indicator.political_impact_countries",
            "impact_indicator.political_impact_countries.code.code",
            "impact_indicator.political_impact_countries.code.subcode",

            "impact_indicator.political_impact.code.code",
            "impact_indicator.political_impact.code.subcode",

            "impact_indicator.political_impact_third_countries.code.code",
            "impact_indicator.political_impact_third_countries.code.subcode",

            "impact_indicator.impact_indicator.code.code",
            "impact_indicator.impact_indicator.code.subcode",

            "impact_indicator.functional_impact.code",
            "impact_indicator.functional_impact.subcode",

            "impact_indicator.intelligence_impact.code",
            "impact_indicator.intelligence_impact.subcode",

            "articles",
            "articles.source",

            "logs",
            "status"
        ],
        "pagination[pageSize]": 100
    })
    return f"{filters}&{nested_query}"


def fetch_data(query, token):
    url = f"{BASE_URL}/?{query}"
    headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    response = req.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_paginated_data(query, token):
    data = []
    initial_response = fetch_data(query, token)
    data.append(initial_response)
    nb_pages = initial_response["meta"]["pagination"]["pageCount"]

    for page in range(2, nb_pages + 1):
        paginated_query = f"{query}&pagination[page]={page}"
        response = fetch_data(paginated_query, token)
        data.append(response)

    return data


def query_database(
        token=None, flag_type=None, flag_status=None, receiver_region=None,
        receiver_country=None, date_type=None, range_start_date=None, range_end_date=None, receiver_category=None,
        initiator_country=None
):
    status_conditions = [("status", "Sent to database"), ("tracker_status", "Sent to tracker")]
    query = build_query(
        flag_type=flag_type, flag_status=flag_status, receiver_region=receiver_region,
        receiver_country=receiver_country, date_type=date_type, range_start_date=range_start_date,
        range_end_date=range_end_date, status_conditions=status_conditions, receiver_category=receiver_category,
        initiator_country=initiator_country
    )
    raw_data = get_paginated_data(query, token)

    all_incidents_data = []
    for page in raw_data:
        for elem in page["data"]:
            incident_data = elem["attributes"]
            incident_data["id"] = elem["id"]
            all_incidents_data.append(incident_data)

    return all_incidents_data
