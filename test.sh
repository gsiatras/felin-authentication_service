curl -X POST http://localhost:8000/new_merchant \
-H "Content-Type: application/json" \
-d '{
    "access_token": "eyJraWQiOiJrYVk1ZTAxTW1cL3UyOXhqZ24zYUEyUVwvMGhDVnJ4SlwvckhqYnlodlExOWdvPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJiMGZjMzlhYy1kMDQxLTcwNDktMDYzMy02YTY5NDJhYmRhZGUiLCJjb2duaXRvOmdyb3VwcyI6WyJldS1ub3J0aC0xX1RnV3VuZzBHeF9GYWNlYm9vayJdLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtbm9ydGgtMS5hbWF6b25hd3MuY29tXC9ldS1ub3J0aC0xX1RnV3VuZzBHeCIsInZlcnNpb24iOjIsImNsaWVudF9pZCI6IjRrbG5hYTZqOTU2Z3Qyc2V0ZDY3MGF0ZWVvIiwib3JpZ2luX2p0aSI6IjM3NzQzMDllLTMyNTAtNDBiNi05OWVmLTBiYmJmNWUzYWZkYiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE3MzEzMTYyOTIsImV4cCI6MTczMTMxOTg5MiwiaWF0IjoxNzMxMzE2MjkyLCJqdGkiOiJjNWQ1NDA0MC0wZTcyLTQ1M2UtOGU1Ny01NWM1ZWFlZWNlYWQiLCJ1c2VybmFtZSI6ImZhY2Vib29rXzg3NzQ1MzE1NjI1OTk1NTQifQ.J2wauosTShQ8uudFvNTQ6JyrQDgQlKWlpXW3dD7RjAqkY3yUua0vhnX8UbvfP7RQBmz5qgEkZsx0CqaKwz1l5UAAhQrufZu1x2ndGByWUrBhMUG9R__DUIvVFiqtQwHu54PP3diGKtQMp5InFTphMqg-lRFKzKIm0jD8-fvNI3hCWUsYF821ZK7oHOR-s7vVP0BETnlAMXCX4BlG_8z8vdG5Z0KHGVFgMrKQNgfAQ_Rz72KrMZpq5yvUygcSiOSh9davUtgNYG8y0lJZYip83fRCjKpHs2wIC4mAatc61O2w1PTgg3-zz8tRQj2sK-Qe0umVte0vapZhBiWBZ4RggQ",
    "country": "CountryName",
    "companyName": "Company Name",
    "afm": "123456789",
    "address": "123 Main St",
    "businessType": "Retail",
    "postalCode": "12345",
    "city": "CityName",
    "phoneNumber": "+1234567890"
}'
