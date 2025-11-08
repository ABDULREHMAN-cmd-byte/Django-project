import random
from blog.models import Supplier, Equipment, StockItem, Inspection, Project

def run():
    # Suppliers
    supplier_names = [
        ("Shell Pakistan", "Refinery"),
        ("Total Energies", "Distributor"),
        ("PSO", "Distributor"),
        ("Sui Northern Gas", "Gas Supplier"),
        ("Hascol Petroleum", "Transporter"),
    ]

    suppliers = []
    for name, ctype in supplier_names:
        s = Supplier.objects.create(
            name=name,
            company_type=ctype,
            contact_person=random.choice(["Ali Khan", "Usman Ahmed", "Bilal Raza"]),
            email=f"{name.lower().replace(' ', '')}@example.com",
            phone=f"+92{random.randint(3000000000, 3999999999)}",
            address=random.choice(["Karachi", "Lahore", "Islamabad"]),
        )
        suppliers.append(s)

    # Equipment
    equipment_list = [
        ("Main Storage Tank A", "Storage Tank", 5000),
        ("Compressor Unit B", "Compressor", 1200),
        ("Pipeline North", "Pipeline", 0),
        ("Fuel Pump C", "Pump", 200),
    ]

    for name, etype, cap in equipment_list:
        Equipment.objects.create(
            name=name,
            type=etype,
            condition=random.choice(["Good", "Needs Repair"]),
            location=random.choice(["Karachi", "Lahore", "Rawalpindi"]),
            storage_capacity=cap,
        )

    # Stock Items
    fuels = ["Petrol", "Diesel", "Natural Gas", "LPG"]
    for fuel in fuels:
        StockItem.objects.create(
            name=f"{fuel} Stock",
            fuel_type=fuel,
            supplier=random.choice(suppliers),
            quantity=random.randint(500, 5000),
            min_level=500,
        )

    # Projects
    for i in range(3):
        Project.objects.create(
            name=f"Pipeline Expansion {i+1}",
            location=random.choice(["Karachi Port", "Multan Terminal", "Gwadar Refinery"]),
            manager=random.choice(["Engr. Ahmed", "Zeeshan", "Khalid"]),
            start_date="2024-01-15",
            active=bool(random.getrandbits(1))
        )

    print("✅ Petroleum dummy data added successfully!")