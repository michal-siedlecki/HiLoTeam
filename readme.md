HiLo Team 

Cel Aplikacji

Utworzenie dwukierunkowego serwera proxy, który umożliwia bezpieczne utworzenie tunelu SSH w prosty sposób. 
Które pozwoli na połączenie za firewallem w sposób bezpieczny i dwukierunkowy urządzeń IOT i aplikacji

Rozwiązanie może być wykorzystane do bezpiecznego i prostego w konfiguracji przesyłu danych w wielu dziedzinach życia:
Madycyna, Przemysł, Nauka

Proces tworzenia takiego połączenia wygląda następująco

1. Użytkownik pobiera kod z repozytorium na kartę sd i wkłada ją do urządzenia IOT
2. Urządzenie uruchamia w sieci lokalnej użytkownika serwer http z lokalnym panelem konfiguracji
2. Użytkownik generuje w lokalnym panelu klucze na raspbiaku i wyświetla mu się klucz publiczny
3. User prosi o rejestrację
4. My tworzymy w bazie credentiale dla użytkownika 
5. Wysyłamy je
6. On wchodzi na panel konfiguracyjny
7. Wkleja klucz publiczny i klika submit
8. Gdy kliknie submit uruchamia skrypt który kopiuje ten klucz do wlasciwego katalogu
9. Następnie użytkownik ze swojego raspiaka nawiązuje połączenie ssh i patrzy w panelu zdalnym czy się udało
10. Jeśli się udało powinien zobaczyć swojego nighscouta wchodząc na swój panel 'publiczny'

Co mamy:
Strona w której zużytkownik generuje klucze dostępu do serwera i wyświetla klucz publiczny 
Użytkownik ma możliwośc przechowania 
-------------------------------------------------
1. Uzytkownik tworzy sobie klucz na swoim urzadzeniu
2. Uzytkownik wysyla prosbe o utworzenie konta
3. Konto zostaje utworzone w MongoDB:
#### db.users.insertOne({name: "nazwa", password: "1234", has_key: ""})
4. Nastepnie zostaje stworzony przez roota na zdalnym serwerze przy uzyciu
####  python3 create_user.py nazwa
5. Uzytkownik wkleja swoje klucz na zdalny serwer
6. Klucz zostaje zapisany w katalogu uzytkownika na zdalnym serwerze
7. Polaczenie zostaje nawiazane