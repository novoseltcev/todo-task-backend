INSERT INTO users (login, email, password, reg_date) VALUES ('st-a-novoseltcev', 'st.a.novoseltcev@mail.ru', 'pbkdf2:sha256:150000$mQRdsHtG$65cbabf4b595cfa09a3bb97747861654e07ae4172a6454d603ed2cf37f6d9d22', '2021-03-10');
INSERT INTO categories (name, user_id) VALUES ('All', 1);
INSERT INTO tasks (title, status, category_id) VALUES ('Do HomeWork by PYTHON', FALSE, 1);
