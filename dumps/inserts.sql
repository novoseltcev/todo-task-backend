INSERT INTO "users" (role, status, email, password) VALUES ('admin', 'common', 'test@test.test', 'pbkdf2:sha256:150000$mQRdsHtG$65cbabf4b595cfa09a3bb97747861654e07ae4172a6454d603ed2cf37f6d9d22');
INSERT INTO "users" (role, status, email, password) VALUES ('common', 'unconfirmed', 'qwerty@mail.ru', 'pbkdf2:sha256:150000$I52KdFI2$6f880c10b849157c9a06dd6453f36c797dbe4da8eeecb8e8aab78780b3f98212');
INSERT INTO categories (name, user_id) VALUES ('Python', 1);
INSERT INTO categories (name, user_id) VALUES ('JS', 1);
INSERT INTO categories (name, user_id) VALUES ('Python', 2);
INSERT INTO tasks (name, status, user_id, category_id) VALUES ('move scrypt exec from crontab to celery', FALSE, 1, 1);
