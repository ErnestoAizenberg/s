from mimesis import File, Person
from mimesis.locales import Locale

audio_file = File()

person = Person(Locale.RU)

full_name = person.full_name()
# Output: 'Brande Sears'

email = person.email(domains=["example.com"])
# Output: 'roccelline1878@example.com'

email2 = person.email(domains=["mimesis.name"], unique=True)
# Output: 'f272a05d39ec46fdac5be4ac7be45f3f@mimesis.name'

telephone = person.telephone(mask="+7##########")
# Output: '1-436-896-5213'
