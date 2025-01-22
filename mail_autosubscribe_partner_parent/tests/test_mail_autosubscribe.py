from odoo_test_helper import FakeModelLoader

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestMailAutosubscribe(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context, tracking_disable=True, test_mail_autosubscribe=True
            )
        )
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models.fake_order import FakeOrder

        cls.loader.update_registry((FakeOrder,))
        cls.fake_order_model = cls.env["ir.model"].search(
            [("model", "=", "fake.order")]
        )
        cls.mail_template = cls.env["mail.template"].create(
            {
                "model_id": cls.fake_order_model.id,
                "name": "Fake Order",
                "subject": "Fake Order: {{object.partner_id.name}}",
                "partner_to": "{{object.partner_id.id}}",
                "body_html": "Fake Order",
            }
        )
        cls.commercial_partner = cls.env.ref("base.res_partner_4")
        cls.partner_1 = cls.env.ref("base.res_partner_address_13")
        cls.partner_2 = cls.env.ref("base.res_partner_address_14")
        cls.partner_3 = cls.env.ref("base.res_partner_address_24")
        cls.autosubscribe_fake_order = cls.env["mail.autosubscribe"].create(
            {"model_id": cls.fake_order_model.id}
        )
        cls.partner_3.mail_autosubscribe_ids = [(4, cls.autosubscribe_fake_order.id)]
        cls.order = cls.env["fake.order"].create({"partner_id": cls.partner_2.id})

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        return super().tearDownClass()

    def test_message_subscribe(self):
        self.assertFalse(self.order.message_partner_ids, "No subscribers yet")
        self.order.message_subscribe([self.order.partner_id.id])
        self.assertEqual(
            self.order.message_partner_ids,
            self.partner_2 | self.partner_3 | self.commercial_partner,
            "Partner 3 is automatically subscribed",
        )
