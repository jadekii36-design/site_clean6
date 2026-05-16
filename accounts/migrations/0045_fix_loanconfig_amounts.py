from decimal import Decimal

from django.db import migrations


def set_loan_amounts(apps, schema_editor):
    LoanConfig = apps.get_model("accounts", "LoanConfig")
    new_min = Decimal("40000.00")
    new_max = Decimal("2000000.00")

    cfg = LoanConfig.objects.first()
    if cfg is None:
        LoanConfig.objects.create(min_amount=new_min, max_amount=new_max)
    else:
        LoanConfig.objects.update(min_amount=new_min, max_amount=new_max)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0044_alter_user_account_status"),
    ]

    operations = [
        migrations.RunPython(set_loan_amounts, noop),
    ]
