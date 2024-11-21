from faker import Faker
import random
fake = Faker(locale="fr_FR")

# nom = fake.name()
# print(nom)

# email = fake.ascii_email()
# print(email)
# for _ in range(5):
#     print(fake.unique.random_int())

# numbers = [fake.unique.random_int() for _ in range(500)]
# for _ in range(5):
#     print(fake.name())
#     print(fake.address())
#     print(fake.text())
#     print("*****")

print((fake.unique.numerify(text='%%%%%%%%%%')))

l_specialite = ["Yoga", "Pump", "Pilates", "Musculation", "Boxe"]
print(random.choice(l_specialite))