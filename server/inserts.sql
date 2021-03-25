INSERT INTO users (role, login, email, password, reg_date) VALUES ('owner', 'st-a-novoseltcev', 'st.a.novoseltcev@mail.ru', 'pbkdf2:sha256:150000$mQRdsHtG$65cbabf4b595cfa09a3bb97747861654e07ae4172a6454d603ed2cf37f6d9d22', '2021-03-10');
INSERT INTO users (role,login, email, password, reg_date) VALUES ('customer', 'qwerty', 'qwerty@mail.ru', 'pbkdf2:sha256:150000$I52KdFI2$6f880c10b849157c9a06dd6453f36c797dbe4da8eeecb8e8aab78780b3f98212', '2021-03-19');
INSERT INTO categories (name, id_user) VALUES ('Python', 1);
INSERT INTO categories (name, id_user) VALUES ('JS', 2);
INSERT INTO tasks (title, status, id_user, id_category) VALUES ('Do HomeWork by JWT', FALSE, 1, 1);