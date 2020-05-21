import sys
from typing import List
from datetime import datetime
from exceptions import MissingEntityException, InvalidEntityException


class StreamModel(object):
    VALUE_NOT_SET = 'value_not_set'
    salesforce_datetime_format = '%Y-%m-%dT%H:%M:%S.%f%z'
    mysql_datetime_format = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def datetimeify(cls, datetime_string: str):
        return datetime.strptime(datetime_string, cls.salesforce_datetime_format).strftime(cls.mysql_datetime_format) if datetime_string is not None else None

    @classmethod
    def intify(cls, int_string: str):
        return int(int_string) if int_string else None

    @classmethod
    def get_entity(cls, stream_data):

        entity_type = stream_data.get('data').get('attributes').get('type')

        if not entity_type:
            raise MissingEntityException('A data -> attributes -> type must submitted.')

        this_module = sys.modules[__name__]

        try:
            cls_ = getattr(this_module, entity_type)
        except AttributeError:
            raise InvalidEntityException(f'There is no class definition that corresponds to the entity type {entity_type}')
        else:
            return cls_(**stream_data.get('data'))

    @classmethod
    def get_action_type(cls, stream_data):
        return stream_data.get('action')

    @classmethod
    def get_record_source(cls, stream_data):
        return stream_data.get('recordSource')

    def set_from_alias(self, field_name: str, aliases: list, kwargs):
        """
        get first non VALUE_NOT_SET value from a dictionary

        :param field_name: the field_name to set
        :param aliases: the list of aliases to check against the kwargs passed in
        :param kwargs: the kwargs to use to set
        :return:
        """

        for alias in aliases:
            if kwargs.get(alias, self.VALUE_NOT_SET) != self.VALUE_NOT_SET:
                setattr(self, field_name, kwargs.get(alias))
                return

        return

class CountyOffice(StreamModel):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', self.VALUE_NOT_SET)


class ShippingAddress(StreamModel):
    def __init__(self, **kwargs):
        self.city = kwargs.get('city', self.VALUE_NOT_SET)
        self.country = kwargs.get('country', self.VALUE_NOT_SET)
        self.latitude = kwargs.get('latitude', self.VALUE_NOT_SET)
        self.longitude = kwargs.get('longitude', self.VALUE_NOT_SET)
        self.postalCode = kwargs.get('postalCode', self.VALUE_NOT_SET)
        self.state = kwargs.get('state', self.VALUE_NOT_SET)
        self.street = kwargs.get('street', self.VALUE_NOT_SET)


class Account(StreamModel):
    def __init__(self, **kwargs):
        self.uuid = kwargs.get('uuid', self.VALUE_NOT_SET)
        self.track_id = kwargs.get('track_id', self.VALUE_NOT_SET) # to be removed once we are all on uuids
        self.state: State = State(**kwargs.get('state')) if kwargs.get('state') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.county_office = CountyOffice(**kwargs.get('county_office', self.VALUE_NOT_SET)) if kwargs.get('county_office') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.parent_account = Account(**kwargs.get('parent_account', self.VALUE_NOT_SET)) if kwargs.get('parent_account') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.type = kwargs.get('type', self.VALUE_NOT_SET)
        self.name = kwargs.get('name', self.VALUE_NOT_SET)
        self.address = kwargs.get('address', self.VALUE_NOT_SET)
        self.city = kwargs.get('city', self.VALUE_NOT_SET)
        self.zip = kwargs.get('zip', self.VALUE_NOT_SET)
        self.phone1 = kwargs.get('phone1', self.VALUE_NOT_SET)
        self.phone2 = kwargs.get('phone2', self.VALUE_NOT_SET)
        self.fax = kwargs.get('fax', self.VALUE_NOT_SET)
        self.email = kwargs.get('email', self.VALUE_NOT_SET)
        self.latitude = kwargs.get('latitude', self.VALUE_NOT_SET)
        self.longitude = kwargs.get('longitude', self.VALUE_NOT_SET)
        self.shipping_address: ShippingAddress = ShippingAddress(**kwargs.get('shipping_address')) if kwargs.get('shipping_address') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.created_by_user_uuid = kwargs.get('created_by_user_uuid', self.VALUE_NOT_SET)
        self.modified_by_user_uuid = kwargs.get('modified_by_user_uuid', self.VALUE_NOT_SET)
        self.record_owner_user_uuid = kwargs.get('record_owner_user_uuid', self.VALUE_NOT_SET)
        self.record_type_name = kwargs.get('record_type_name', self.VALUE_NOT_SET)
        self.attributes = {'type': 'Account'}


class AccountContactRelation(StreamModel):
    def __init__(self, **kwargs):
        self.uuid = kwargs.get('uuid', self.VALUE_NOT_SET)
        self.gets_sr = kwargs.get('gets_sr', self.VALUE_NOT_SET)
        self.gets_referral_confirmation = kwargs.get('gets_referral_confirmation', self.VALUE_NOT_SET)
        self.created_by_user_uuid = kwargs.get('created_by_user_uuid', self.VALUE_NOT_SET)
        self.created_date = kwargs.get('created_date', self.VALUE_NOT_SET)
        self.modified_by_user_uuid = kwargs.get('modified_by_user_uuid', self.VALUE_NOT_SET)
        self.last_modified_date = kwargs.get('last_modified_date', self.VALUE_NOT_SET)
        self.is_direct = kwargs.get('is_direct', self.VALUE_NOT_SET)
        self.contact = Contact(**kwargs.get('contact')) if kwargs.get('contact') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.account = Account(**kwargs.get('account')) if kwargs.get('account') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.attributes = {'type': 'AccountContactRelation'}


class Contact(StreamModel):
    def __init__(self, **kwargs):
        self.uuid = kwargs.get('uuid', self.VALUE_NOT_SET)
        self.track_id = kwargs.get('track_id', self.VALUE_NOT_SET)  # to be removed once we are all on uuids
        self.click_to_call = kwargs.get('click_to_call', self.VALUE_NOT_SET)
        self.clickable_phone = kwargs.get('clickable_phone', self.VALUE_NOT_SET)
        self.relation_score_id = kwargs.get('relation_score_id', self.VALUE_NOT_SET)
        self.position = kwargs.get('position', self.VALUE_NOT_SET)
        self.old_position = kwargs.get('old_position', self.VALUE_NOT_SET)
        self.notes = kwargs.get('notes', self.VALUE_NOT_SET)
        self.name = kwargs.get('name', self.VALUE_NOT_SET)
        self.account = Account(**kwargs.get('account')) if kwargs.get('account') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.no_longer_employed_at_facility = kwargs.get('no_longer_employed_at_facility', self.VALUE_NOT_SET)
        self.marital_status = kwargs.get('marital_status', self.VALUE_NOT_SET)
        self.is_marketer = kwargs.get('is_marketer', self.VALUE_NOT_SET)
        self.is_keycontact = kwargs.get('is_keycontact', self.VALUE_NOT_SET)
        self.is_corporate = kwargs.get('is_corporate', self.VALUE_NOT_SET)
        self.gets_sr = kwargs.get('gets_sr', self.VALUE_NOT_SET)
        self.gets_referral_confirmation = kwargs.get('gets_referral_confirmation', self.VALUE_NOT_SET)
        self.full_name = kwargs.get('full_name', self.VALUE_NOT_SET)
        self.extension = kwargs.get('extension', self.VALUE_NOT_SET)
        self.jigsaw_contact_id = kwargs.get('jigsaw_contact_id', self.VALUE_NOT_SET)
        self.jigsaw = kwargs.get('jigsaw', self.VALUE_NOT_SET)
        self.photo_url = kwargs.get('photo_url', self.VALUE_NOT_SET)
        self.do_not_call = kwargs.get('do_not_call', self.VALUE_NOT_SET)
        self.has_opted_out_of_fax = kwargs.get('has_opted_out_of_fax', self.VALUE_NOT_SET)
        self.has_opted_out_of_email = kwargs.get('has_opted_out_of_email', self.VALUE_NOT_SET)
        self.salesforce_owner_id = kwargs.get('salesforce_owner_id', self.VALUE_NOT_SET)
        self.description = kwargs.get('description', self.VALUE_NOT_SET)
        self.birthdate = kwargs.get('birthdate', self.VALUE_NOT_SET)
        self.lead_source = kwargs.get('lead_source', self.VALUE_NOT_SET)
        self.assistant_name = kwargs.get('assistant_name', self.VALUE_NOT_SET)
        self.department = kwargs.get('department', self.VALUE_NOT_SET)
        self.title = kwargs.get('title', self.VALUE_NOT_SET)
        self.email = kwargs.get('email', self.VALUE_NOT_SET)
        self.reports_to_id = kwargs.get('reports_to_id', self.VALUE_NOT_SET)
        self.assistant_phone = kwargs.get('assistant_phone', self.VALUE_NOT_SET)
        self.other_phone = kwargs.get('other_phone', self.VALUE_NOT_SET)
        self.home_phone = kwargs.get('home_phone', self.VALUE_NOT_SET)
        self.mobile_phone = kwargs.get('mobile_phone', self.VALUE_NOT_SET)
        self.fax = kwargs.get('fax', self.VALUE_NOT_SET)
        self.phone = kwargs.get('phone', self.VALUE_NOT_SET)
        self.mailing_address = kwargs.get('mailing_address', self.VALUE_NOT_SET)
        self.mailing_street = kwargs.get('mailing_street', self.VALUE_NOT_SET)
        self.mailing_country = kwargs.get('mailing_country', self.VALUE_NOT_SET)
        self.mailing_postalcode = kwargs.get('mailing_postalcode', self.VALUE_NOT_SET)
        self.mailing_state = kwargs.get('mailing_state', self.VALUE_NOT_SET)
        self.mailing_city = kwargs.get('mailing_city', self.VALUE_NOT_SET)
        self.other_address = kwargs.get('other_address', self.VALUE_NOT_SET)
        self.other_country = kwargs.get('other_country', self.VALUE_NOT_SET)
        self.other_postalcode = kwargs.get('other_postalcode', self.VALUE_NOT_SET)
        self.other_state = kwargs.get('other_state', self.VALUE_NOT_SET)
        self.other_city = kwargs.get('other_city', self.VALUE_NOT_SET)
        self.other_street = kwargs.get('other_street', self.VALUE_NOT_SET)
        self.salutation = kwargs.get('salutation', self.VALUE_NOT_SET)
        self.first_name = kwargs.get('first_name', self.VALUE_NOT_SET)
        self.last_name = kwargs.get('last_name', self.VALUE_NOT_SET)
        self.account_salesforce_id = kwargs.get('account_salesforce_id', self.VALUE_NOT_SET)
        self.is_deleted = kwargs.get('is_deleted', self.VALUE_NOT_SET)
        self.attributes = {'type': 'Contact'}


# TODO pass each object or nested Referral?
class Referral(StreamModel):
    def __init__(self, **kwargs):
        self.applicant: Applicant = Applicant(**kwargs.get('applicant')) if kwargs.get('applicant') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.referring_contact: Contact = Contact(**kwargs.get('referring_contact')) if kwargs.get('referring_contact') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.referring_party: Account = Account(**kwargs.get('referring_party')) if kwargs.get('referring_party') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.uuid = kwargs.get('uuid')
        self.applicant_uuid = kwargs.get('applicant_uuid', self.VALUE_NOT_SET)
        self.assigned_to_cm = kwargs.get('assigned_to_cm', self.VALUE_NOT_SET)
        self.coverage_type = kwargs.get('coverage_type', self.VALUE_NOT_SET)
        self.created_by: User = User(**kwargs.get('created_by')) if kwargs.get('created_by') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.created_date = kwargs.get('created_date', self.VALUE_NOT_SET)
        self.follow_up_date = kwargs.get('follow_up_date', self.VALUE_NOT_SET)
        self.date_referral_received = kwargs.get('date_referral_received', self.VALUE_NOT_SET)
        self.deceased = kwargs.get('deceased', self.VALUE_NOT_SET)
        self.expecting_our_call = kwargs.get('expecting_our_call', self.VALUE_NOT_SET)
        self.facility_approval_date = kwargs.get('facility_approval_date', self.VALUE_NOT_SET)
        self.facility_pay_amount = kwargs.get('facility_pay_amount', self.VALUE_NOT_SET)
        # TODO Is this a Model?
        self.facility_pay_approver = User(**kwargs.get('facility_pay_approver', self.VALUE_NOT_SET))  if kwargs.get('facility_pay_approver') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.facility_pay_comment = kwargs.get('facility_pay_comment', self.VALUE_NOT_SET)
        self.facility_pay_confirmed = kwargs.get('facility_pay_confirmed', self.VALUE_NOT_SET)
        self.facility_payment_date = kwargs.get('facility_payment_date', self.VALUE_NOT_SET)
        self.facility_pay_entered_by = User(**kwargs.get('facility_pay_entered_by', self.VALUE_NOT_SET))  if kwargs.get('facility_pay_entered_by') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.facility_pay_updated_at = kwargs.get('facility_pay_updated_at', self.VALUE_NOT_SET)
        self.form_of_payment = kwargs.get('form_of_payment', self.VALUE_NOT_SET)
        self.gifting = kwargs.get('gifting', self.VALUE_NOT_SET)
        self.has_liquid_assets = kwargs.get('has_liquid_assets', self.VALUE_NOT_SET)
        self.has_appointment = kwargs.get('has_appointment', self.VALUE_NOT_SET)
        self.income = kwargs.get('income', self.VALUE_NOT_SET)
        self.info_packet_shipping_company = kwargs.get('info_packet_shipping_company', self.VALUE_NOT_SET)
        self.info_packet_tracking_number = kwargs.get('info_packet_tracking_number', self.VALUE_NOT_SET)
        self.info_packet_track_status = kwargs.get('info_packet_track_status', self.VALUE_NOT_SET)
        self.initial_contact_attempts = kwargs.get('initial_contact_attempts', self.VALUE_NOT_SET)
        self.intake_rep: User = User(**kwargs.get('intake_rep')) if kwargs.get('intake_rep') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.is_community = kwargs.get('is_community', self.VALUE_NOT_SET)
        self.is_confirmed = kwargs.get('is_confirmed', self.VALUE_NOT_SET)
        self.field_appointment_datetime = kwargs.get('field_appointment_datetime', self.VALUE_NOT_SET)
        self.is_deleted = kwargs.get('is_deleted', self.VALUE_NOT_SET)
        self.last_modified_by: User = User(**kwargs.get('last_modified_by')) if kwargs.get('last_modified_by') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.last_modified_date = kwargs.get('last_modified_date', self.VALUE_NOT_SET)
        self.liquid_assets_amount = kwargs.get('liquid_assets_amount', self.VALUE_NOT_SET)
        self.long_term_care_plan = kwargs.get('long_term_care_plan', self.VALUE_NOT_SET)
        self.marketing_rep: User = User(**kwargs.get('marketing_rep')) if kwargs.get('marketing_rep') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.medicaid_case_type = kwargs.get('medicaid_case_type', self.VALUE_NOT_SET)
        self.needs_medicaid_urgently = kwargs.get('needs_medicaid_urgently', self.VALUE_NOT_SET)
        self.non_liquid_assets = kwargs.get('non_liquid_assets', self.VALUE_NOT_SET)
        self.no_status_reports = kwargs.get('no_status_reports', self.VALUE_NOT_SET)
        self.not_pursuing_reason = kwargs.get('not_pursuing_reason', self.VALUE_NOT_SET)
        self.other_amount = kwargs.get('other_amount', self.VALUE_NOT_SET)
        self.owns_home = kwargs.get('owns_home', self.VALUE_NOT_SET)
        self.pay_type = kwargs.get('pay_type', self.VALUE_NOT_SET)
        self.pending_follow_up_date = kwargs.get('pending_follow_up_date', self.VALUE_NOT_SET)
        self.pending_reason = kwargs.get('pending_reason', self.VALUE_NOT_SET)
        self.pension_amount1 = kwargs.get('pension_amount1', self.VALUE_NOT_SET)
        self.pension_amount2 = kwargs.get('pension_amount2', self.VALUE_NOT_SET)
        self.prepaid_burial = kwargs.get('prepaid_burial', self.VALUE_NOT_SET)
        self.private_pay_amount = kwargs.get('private_pay_amount', self.VALUE_NOT_SET)
        self.private_pay_comment = kwargs.get('private_pay_comment', self.VALUE_NOT_SET)
        self.private_pay_entered_by = User(**kwargs.get('private_pay_entered_by', self.VALUE_NOT_SET))  if kwargs.get('private_pay_entered_by') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.private_pay_updated_at = kwargs.get('private_pay_updated_at', self.VALUE_NOT_SET)
        self.record_type_id = kwargs.get('record_type_id', self.VALUE_NOT_SET)
        self.referral_confirmation = kwargs.get('referral_confirmation', self.VALUE_NOT_SET)
        self.referral_link = kwargs.get('referral_link', self.VALUE_NOT_SET)
        self.referral_method = kwargs.get('referral_method', self.VALUE_NOT_SET)
        self.referrer_notes = kwargs.get('referrer_notes', self.VALUE_NOT_SET)
        self.rental_amount = kwargs.get('rental_amount', self.VALUE_NOT_SET)
        self.social_security_amount = kwargs.get('social_security_amount', self.VALUE_NOT_SET)
        self.spend_down = kwargs.get('spend_down', self.VALUE_NOT_SET)
        self.sps_fee_amount = kwargs.get('sps_fee_amount', self.VALUE_NOT_SET)
        self.state_of_service: State = State(**kwargs.get('state_of_service')) if kwargs.get('state_of_service') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.status = kwargs.get('status', self.VALUE_NOT_SET)
        self.status_track_style = kwargs.get('status_track_style', self.VALUE_NOT_SET)
        self.status_report_comment = kwargs.get('status_report_comment', self.VALUE_NOT_SET)
        self.time_to_call = kwargs.get('time_to_call', self.VALUE_NOT_SET)
        self.track_id = kwargs.get('track_id', self.VALUE_NOT_SET)
        self.unprocessed_applicant_name = kwargs.get('unprocessed_applicant_name', self.VALUE_NOT_SET)
        self.unprocessed_facility_contact_email = kwargs.get('unprocessed_facility_contact_email', self.VALUE_NOT_SET)
        self.unprocessed_referral_data = kwargs.get('unprocessed_referral_data', self.VALUE_NOT_SET)
        self.who_is_not_pursuing = kwargs.get('who_is_not_pursuing', self.VALUE_NOT_SET)
        self.attributes = {'type': 'Referral'}


class Applicant(StreamModel):
    def __init__(self, **kwargs):
        self.related_applicant_contacts: List[RelatedApplicantContact] = [RelatedApplicantContact(**related_applicant_contact) for related_applicant_contact in kwargs.get('related_applicant_contacts')] if kwargs.get('related_applicant_contacts') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.uuid = kwargs.get('uuid', self.VALUE_NOT_SET)
        self.cell_phone = kwargs.get('cell_phone', self.VALUE_NOT_SET)
        self.city = kwargs.get('city', self.VALUE_NOT_SET)
        self.created_by: User = User(**kwargs.get('created_by')) if kwargs.get('created_by') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.created_date = kwargs.get('created_date', self.VALUE_NOT_SET)
        self.current_facility: Account = Account(**kwargs.get('current_facility')) if kwargs.get('current_facility') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.email = kwargs.get('email', self.VALUE_NOT_SET)
        self.case_manager: User = User(**kwargs.get('case_manager')) if kwargs.get('case_manager') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.first_name = kwargs.get('first_name', self.VALUE_NOT_SET)
        self.home_phone = kwargs.get('home_phone', self.VALUE_NOT_SET)
        self.is_deleted = kwargs.get('is_deleted', self.VALUE_NOT_SET)
        self.is_us_citizen = kwargs.get('is_us_citizen', self.VALUE_NOT_SET)
        self.last_modified_by: User = User(**kwargs.get('last_modified_by')) if kwargs.get('last_modified_by') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.last_modified_date = kwargs.get('last_modified_date', self.VALUE_NOT_SET)
        self.last_name = kwargs.get('last_name', self.VALUE_NOT_SET)
        self.marital_status = kwargs.get('marital_status', self.VALUE_NOT_SET)
        self.other_phone = kwargs.get('other_phone', self.VALUE_NOT_SET)
        self.personality = kwargs.get('personality', self.VALUE_NOT_SET)
        self.residency = kwargs.get('residency', self.VALUE_NOT_SET)
        self.state: State = State(**kwargs.get('state')) if kwargs.get('state') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.status = kwargs.get('status', self.VALUE_NOT_SET)
        self.street1 = kwargs.get('street1', self.VALUE_NOT_SET)
        self.street2 = kwargs.get('street2', self.VALUE_NOT_SET)
        self.track_id = kwargs.get('track_id', self.VALUE_NOT_SET)
        self.zip = kwargs.get('zip', self.VALUE_NOT_SET)
        self.attributes = {'type': 'Applicant'}


class ApplicantContact(StreamModel):
    def __init__(self, **kwargs):
        self.uuid = kwargs.get('uuid', self.VALUE_NOT_SET)
        self.applicant_uuid = kwargs.get('applicant_uuid', self.VALUE_NOT_SET)
        self.cell_phone = kwargs.get('cell_phone', self.VALUE_NOT_SET)
        self.city = kwargs.get('city', self.VALUE_NOT_SET)
        self.created_by: User = User(**kwargs.get('created_by')) if kwargs.get('created_by') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.created_date = kwargs.get('created_date', self.VALUE_NOT_SET)
        self.email = kwargs.get('email', self.VALUE_NOT_SET)
        self.fax = kwargs.get('fax', self.VALUE_NOT_SET)
        self.first_name = kwargs.get('first_name', self.VALUE_NOT_SET)
        self.name = kwargs.get('first_name', self.VALUE_NOT_SET)
        self.home_phone = kwargs.get('home_phone', self.VALUE_NOT_SET)
        self.is_deleted = kwargs.get('is_deleted', self.VALUE_NOT_SET)
        self.last_modified_by: User = User(**kwargs.get('last_modified_by')) if kwargs.get('last_modified_by') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.last_modified_date = kwargs.get('last_modified_date', self.VALUE_NOT_SET)
        self.last_name = kwargs.get('last_name', self.VALUE_NOT_SET)
        self.other_phone = kwargs.get('other_phone', self.VALUE_NOT_SET)
        self.state: State = State(**kwargs.get('state')) if kwargs.get('state') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.street1 = kwargs.get('street1', self.VALUE_NOT_SET)
        self.street2 = kwargs.get('street2', self.VALUE_NOT_SET)
        self.zip = kwargs.get('zip', self.VALUE_NOT_SET)
        self.attributes = {'type': 'ApplicantContact'}


class RelatedApplicantContact(StreamModel):
    def __init__(self, **kwargs):
        self.uuid = kwargs.get('uuid', self.VALUE_NOT_SET)
        self.applicant: Applicant = Applicant(**kwargs.get('applicant')) if kwargs.get('applicant') not in (
            None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.applicant_contact: ApplicantContact = ApplicantContact(**kwargs.get('applicant_contact')) if kwargs.get(
            'applicant_contact') not in (
              None,
              self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.created_by: User = User(**kwargs.get('created_by')) if kwargs.get('created_by') not in (
            None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET

        self.created_date = kwargs.get('created_date', self.VALUE_NOT_SET)
        self.is_deleted = kwargs.get('is_deleted', self.VALUE_NOT_SET)
        self.is_power_of_attorney = kwargs.get('is_power_of_attorney', self.VALUE_NOT_SET)
        self.is_primary = kwargs.get('is_primary', self.VALUE_NOT_SET)
        self.is_spouse = kwargs.get('is_spouse', self.VALUE_NOT_SET)
        self.last_modified_by: User = User(**kwargs.get('last_modified_by')) if kwargs.get('last_modified_by') not in (
            None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET

        self.last_modified_date = kwargs.get('last_modified_date', self.VALUE_NOT_SET)
        self.relationship = kwargs.get('relationship', self.VALUE_NOT_SET)
        self.applicant_uuid = kwargs.get('applicant_uuid', self.VALUE_NOT_SET)
        self.attributes = {'type': 'RelatedApplicantContact'}


class State(StreamModel):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', self.VALUE_NOT_SET)
        self.abbreviation = kwargs.get('abbreviation', self.VALUE_NOT_SET)

        self.set_from_alias('abbreviation', ['abbr'], kwargs=kwargs)


class User(StreamModel):
    def __init__(self, **kwargs):
        self.track_id = kwargs.get('track_id', self.VALUE_NOT_SET)
        self.mobile = kwargs.get('mobile', self.VALUE_NOT_SET)
        self.extension = kwargs.get('extension', self.VALUE_NOT_SET)
        self.fax = kwargs.get('fax', self.VALUE_NOT_SET)
        self.alias = kwargs.get('nickname', self.VALUE_NOT_SET)
        self.uuid = kwargs.get('uuid', self.VALUE_NOT_SET)
        self.first_name = kwargs.get('first_name', self.VALUE_NOT_SET)
        self.last_name = kwargs.get('last_name', self.VALUE_NOT_SET)
        self.email = kwargs.get('email', self.VALUE_NOT_SET)
        self.phone = kwargs.get('phone', self.VALUE_NOT_SET)


class Task(StreamModel):
    def __init__(self, **kwargs):
        self.assignee_uuid = kwargs.get('assignee_uuid', self.VALUE_NOT_SET)
        self.attributes = {'type': 'Task'}
        self.created_by = kwargs.get('created_by') if kwargs.get('created_by') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.deleted_by = kwargs.get('deleted_by') if kwargs.get('deleted_by') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.last_modified_by = kwargs.get('last_modified_by') if kwargs.get('last_modified_by') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.description = kwargs.get('description', self.VALUE_NOT_SET)
        self.subject = kwargs.get('subject', self.VALUE_NOT_SET)
        self.uuid = kwargs.get('uuid', self.VALUE_NOT_SET)
        self.what_uuid = kwargs.get('what_uuid', self.VALUE_NOT_SET)
        self.what_type = kwargs.get('what_type', self.VALUE_NOT_SET)
        self.status = kwargs.get('status', self.VALUE_NOT_SET)


class Event(StreamModel):
    def __init__(self, **kwargs):
        self.attributes = {'type': 'Event'}
        self.description = kwargs.get('description', self.VALUE_NOT_SET)
        self.duration_in_minutes = kwargs.get('duration_in_minutes', self.VALUE_NOT_SET)
        self.end_date_time_utc = kwargs.get('end_date_time_utc', self.VALUE_NOT_SET)
        self.owner_uuid = kwargs.get('owner_uuid', self.VALUE_NOT_SET)
        self.subject = kwargs.get('subject', self.VALUE_NOT_SET)
        self.uuid = kwargs.get('uuid', self.VALUE_NOT_SET)
        self.what_uuid = kwargs.get('what_uuid', self.VALUE_NOT_SET)
        self.what_type = kwargs.get('what_type', self.VALUE_NOT_SET)
        self.who_uuids = kwargs.get('who_uuids', self.VALUE_NOT_SET)
        self.date_completed = kwargs.get('date_completed', self.VALUE_NOT_SET)


class FieldRepAppointment(StreamModel):
    def __init__(self, **kwargs):
        self.uuid = kwargs.get('uuid', self.VALUE_NOT_SET)
        self.created_at = kwargs.get('created_at', self.VALUE_NOT_SET)
        self.updated_at = kwargs.get('updated_at', self.VALUE_NOT_SET)
        self.in_person = kwargs.get('in_person', self.VALUE_NOT_SET)
        self.day = kwargs.get('day', self.VALUE_NOT_SET)
        self.is_private = kwargs.get('is_private', self.VALUE_NOT_SET)
        self.description = kwargs.get('description', self.VALUE_NOT_SET)
        self.end_datetime = kwargs.get('end_datetime', self.VALUE_NOT_SET)
        self.start_datetime = kwargs.get('start_datetime', self.VALUE_NOT_SET)
        self.duration_in_minutes = kwargs.get('duration_in_minutes', self.VALUE_NOT_SET)
        self.activity_date = kwargs.get('activity_date', self.VALUE_NOT_SET)
        self.activity_datetime = kwargs.get('activity_datetime', self.VALUE_NOT_SET)
        self.location = kwargs.get('location', self.VALUE_NOT_SET)
        self.subject = kwargs.get('subject', self.VALUE_NOT_SET)
        self.application: FieldRepApplication = FieldRepApplication(**kwargs.get('application')) if kwargs.get('application') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.referral: Referral = Referral(**kwargs.get('referral')) if kwargs.get('referral') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.referring_party: Account = Account(**kwargs.get('referring_party')) if kwargs.get('referring_party') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.external_applicant_track_id = kwargs.get('external_applicant_track_id', self.VALUE_NOT_SET)
        self.attributes = {'type': 'FieldRepAppointment'}


class FieldRepApplication(StreamModel):
    def __init__(self, **kwargs):
        self.uuid = kwargs.get('uuid', self.VALUE_NOT_SET)
        self.external_applicant_uuid = kwargs.get('external_applicant_uuid', self.VALUE_NOT_SET)
        self.county = kwargs.get('county', self.VALUE_NOT_SET)
        self.state: State = State(**kwargs.get('state')) if kwargs.get('state') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.field_rep_user: User = User(**kwargs.get('field_rep_user')) if kwargs.get('field_rep_user') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.status = kwargs.get('status', self.VALUE_NOT_SET)
        self.medicaid_details: List[MedicaidDetail] = [MedicaidDetail(**medicaid_detail) for medicaid_detail in kwargs.get('medicaid_details')] if kwargs.get('medicaid_details') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.created_at = kwargs.get('created_at', self.VALUE_NOT_SET)
        self.updated_at = kwargs.get('updated_at', self.VALUE_NOT_SET)
        self.attribute_name = {'type': 'FieldRepApplication'}


class TurbocaidApplication(StreamModel):
    def __init__(self, **kwargs):
        self.event_id = kwargs.get('event_id', self.VALUE_NOT_SET)
        self.uuid = kwargs.get('uuid', self.VALUE_NOT_SET)
        self.county = kwargs.get('county', self.VALUE_NOT_SET)
        self.state: State = State(**kwargs.get('state')) if kwargs.get('state') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.status = kwargs.get('status', self.VALUE_NOT_SET)
        self.medicaid_details: List[MedicaidDetail] = [MedicaidDetail(**medicaid_detail) for medicaid_detail in kwargs.get('medicaid_details')] if kwargs.get('medicaid_details') not in (None, self.VALUE_NOT_SET) else self.VALUE_NOT_SET
        self.created_at = kwargs.get('created_at', self.VALUE_NOT_SET)
        self.updated_at = kwargs.get('updated_at', self.VALUE_NOT_SET)
        self.attribute_name = {'type': 'TurbocaidApplication'}


class MedicaidDetail(StreamModel):
    def __init__(self, **kwargs):
        self.event_id = kwargs.get('event_id', self.VALUE_NOT_SET)
        self.uuid = kwargs.get('uuid', self.VALUE_NOT_SET)
        self.attribute_name = kwargs.get('attribute_name', self.VALUE_NOT_SET)
        self.attribute_value = kwargs.get('attribute_value', self.VALUE_NOT_SET)
        self.medicaid_detail_type = kwargs.get('medicaid_detail_type', self.VALUE_NOT_SET)
        self.created_at = kwargs.get('created_at', self.VALUE_NOT_SET)
        self.updated_at = kwargs.get('updated_at', self.VALUE_NOT_SET)
        self.attributes = {'type': 'MedicaidDetail'}
