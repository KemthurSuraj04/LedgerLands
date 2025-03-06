from django.db import models

class User(models.Model):
    address=models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=255)
    aadhar_number = models.CharField(max_length=12, unique=True)  # Aadhar number should be unique
    pan_number = models.CharField(max_length=10, unique=True)  # PAN number should be unique
    document = models.CharField(max_length=255)  # This could be a file field or string, based on your use case
    email = models.EmailField(unique=True)  # Email should be unique
    password = models.CharField(max_length=255)  # You may want to hash the password before storing
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Landreg(models.Model):
    id = models.AutoField(primary_key=True)
    area = models.PositiveIntegerField()  # Area in square meters or other unit
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    land_price = models.PositiveIntegerField()
    property_pid = models.PositiveIntegerField(unique=True)  # Property PID should be unique
    physical_survey_number = models.PositiveIntegerField()
    ipfs_hash = models.CharField(max_length=255)  # Store IPFS hash for referencing the document
    document = models.CharField(max_length=255)  # You can store a file reference or path here
    is_verified = models.BooleanField(default=False)
    is_for_sale = models.BooleanField(default=False)

    def __str__(self):
        return f"Land ID: {self.id} - {self.city}, {self.state}"
