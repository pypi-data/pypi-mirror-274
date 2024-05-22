from typing import NamedTuple

from getopenpay import ApiClient, Configuration
from getopenpay.api import (
  AccountsApi, AuthenticationApi, BillingPortalApi, ChargesApi, CheckoutApi, CouponsApi,
  CreditNotesApi, CustomersApi, EventsApi, InvitesApi, InvoiceItemsApi, InvoicesApi,
  PaymentMethodsApi, PricesApi, ProcessorsApi, ProductFamilyApi, ProductsApi, PromotionCodesApi,
  RefundsApi, SubscriptionItemsApi, SubscriptionsApi, TaxIntegrationsApi, TransitionEligibilityApi,
  UsersApi
)


class ApiKeys(NamedTuple):
  publishable_key: str
  secret_key: str


class OpenPayClient:

  def __init__(self, api_keys: ApiKeys, host: str = 'http://localhost:8000'):
    self.api_keys = api_keys
    self.config = Configuration()
    self.config.host = host
    self.api_client = ApiClient(configuration=self.config)
    self.api_client.set_default_header('X-Publishable-Token', api_keys.publishable_key)
    self.api_client.set_default_header('Authorization', f'Bearer {api_keys.secret_key}')

  @property
  def accounts(self):
    # note these Apis are reinitialized everytime accounts are called.
    # they have lightweight inits for now
    return AccountsApi(self.api_client)

  @property
  def authentication(self):
    return AuthenticationApi(self.api_client)

  @property
  def coupons(self):
    return CouponsApi(self.api_client)

  @property
  def credit_notes(self):
    return CreditNotesApi(self.api_client)

  @property
  def users(self):
    return UsersApi(self.api_client)

  @property
  def customers(self):
    return CustomersApi(self.api_client)

  @property
  def invites(self):
    return InvitesApi(self.api_client)

  @property
  def invoice_items(self):
    return InvoiceItemsApi(self.api_client)

  @property
  def invoices(self):
    return InvoicesApi(self.api_client)

  @property
  def payment_methods(self):
    return PaymentMethodsApi(self.api_client)

  @property
  def prices(self):
    return PricesApi(self.api_client)

  @property
  def products(self):
    return ProductsApi(self.api_client)

  @property
  def promotion_codes(self):
    return PromotionCodesApi(self.api_client)

  @property
  def refunds(self):
    return RefundsApi(self.api_client)

  @property
  def subscription_items(self):
    return SubscriptionItemsApi(self.api_client)

  @property
  def subscriptions(self):
    return SubscriptionsApi(self.api_client)

  @property
  def charges(self):
    return ChargesApi(self.api_client)

  @property
  def events(self):
    return EventsApi(self.api_client)

  @property
  def transition_eligibility(self):
    return TransitionEligibilityApi(self.api_client)

  @property
  def checkout(self):
    return CheckoutApi(self.api_client)

  @property
  def product_family(self):
    return ProductFamilyApi(self.api_client)

  @property
  def billing_portal(self):
    return BillingPortalApi(self.api_client)

  @property
  def tax_integrations(self):
    return TaxIntegrationsApi(self.api_client)

  @property
  def processor(self):
    return ProcessorsApi(self.api_client)
