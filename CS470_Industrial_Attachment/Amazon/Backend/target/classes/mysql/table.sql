create table if not exists se_project.major
(
    id
    bigint
    unsigned
    auto_increment
    primary
    key,
    major_name
    varchar
(
    20
) not null,
    constraint id
    unique
(
    id
)
    );

create table if not exists se_project.course
(
    course_id
    varchar
(
    20
) not null
    primary key,
    course_name varchar
(
    50
) not null,
    course_kind varchar
(
    20
) not null comment '���ʣ�����/ѡ�ޣ�',
    course_type varchar
(
    20
) not null comment '���ͨʶ���ޡ�ͨʶѡ�ޡ�רҵ���ĵȣ�',
    course_language varchar
(
    2
) not null comment '�����Ӣ�˫�',
    course_count varchar
(
    20
) not null comment '�Ʒַ�ʽ',
    course_score int default 0 not null comment 'ѧ��',
    course_last int not null comment 'ѧʱ',
    course_major varchar
(
    20
) default 'ͨʶͨ��' not null,
    constraint course_major_major_name_fk
    foreign key
(
    course_major
) references se_project.major
(
    major_name
)
    );

create index major_major_name_index
    on se_project.major (major_name);

create
definer = se@`%` trigger se_project.update_user_before_delete_major
    before delete
on se_project.major
    for each row
BEGIN
    -- ����user_major
update user
set user_major = 'ͨʶͨ��'
where user_major = old.major_name;
-- ����teacher_major
update teacher
set teacher_major = 'ͨʶͨ��'
where teacher_major = old.major_name;
END;

create table if not exists se_project.role
(
    role_id
    int
    auto_increment
    primary
    key,
    role_name
    text
    not
    null
);

create table if not exists se_project.teacher
(
    teacher_id
    bigint
    unsigned
    auto_increment
    primary
    key,
    teacher_name
    varchar
(
    20
) not null,
    teacher_mail varchar
(
    20
) null,
    teacher_major varchar
(
    20
) null,
    teacher_type varchar
(
    20
) null comment 'ְ�ƣ����ڡ������ڵȣ�',
    constraint teacher_id
    unique
(
    teacher_id
),
    constraint teacher_major_major_name_fk
    foreign key
(
    teacher_major
) references se_project.major
(
    major_name
)
    );

create table if not exists se_project.schedule
(
    schedule_id
    bigint
    unsigned
    auto_increment
    primary
    key,
    schedule_term
    varchar
(
    6
) not null comment 'ѧ��ѧ��',
    schedule_course varchar
(
    20
) not null,
    schedule_class int not null comment '�༶',
    schedule_group int null comment 'С��',
    schedule_teacher1 varchar
(
    20
) not null,
    schedule_week1 varchar
(
    10
) not null comment '��˫�ܵ����',
    schedule_time1 varchar
(
    11
) not null comment 'ʱ�� e.g. 08:00-09:50',
    schedule_place1 varchar
(
    20
) not null comment '�ص�',
    schedule_teacher2 varchar
(
    20
) null,
    schedule_week2 varchar
(
    10
) null,
    schedule_time2 varchar
(
    11
) null,
    schedule_place2 varchar
(
    20
) null,
    schedule_total int not null comment '����',
    schedule_have int default 0 not null comment '��ѡ',
    constraint schedule_id
    unique
(
    schedule_id
),
    constraint schedule_id_2
    unique
(
    schedule_id
),
    constraint schedule_course_course_id_fk
    foreign key
(
    schedule_course
) references se_project.course
(
    course_id
),
    constraint schedule_teacher_teacher_name_fk
    foreign key
(
    schedule_teacher1
) references se_project.teacher
(
    teacher_name
),
    constraint schedule_teacher_teacher_name_fk_2
    foreign key
(
    schedule_teacher2
) references se_project.teacher
(
    teacher_name
)
    );

create
definer = se@`%` trigger se_project.update_schedule_before_insert_schedule
    before insert
    on se_project.schedule
    for each row
BEGIN
    -- ����schedule_term
    IF
NEW.schedule_term IS NULL THEN
        SET NEW.schedule_term = CONCAT(YEAR(NOW()),
                                       case
                                           when month(NOW()) in (2, 3, 4, 5, 6) then '����'
                                           when month(NOW()) in (7, 8) then '�ļ�'
                                           when month(NOW()) in (9, 10, 11, 12, 1) then '�＾'
                                           end
                                );
END IF;
END;

create index teacher_teacher_name_index
    on se_project.teacher (teacher_name);

create table if not exists se_project.user
(
    user_id
    varchar
(
    8
) not null
    primary key,
    user_name varchar
(
    30
) not null,
    user_password text not null,
    user_img text null,
    user_mail varchar
(
    28
) not null,
    user_major varchar
(
    20
) default 'ͨʶͨ��' not null,
    user_valid tinyint null,
    constraint userEmail
    unique
(
    user_mail
),
    constraint userID
    unique
(
    user_id
),
    constraint user_major_major_name_fk
    foreign key
(
    user_major
) references se_project.major
(
    major_name
)
    );

create table if not exists se_project.chosen
(
    chosen_id
    bigint
    unsigned
    auto_increment
    primary
    key,
    chosen_student
    varchar
(
    8
) not null,
    chosen_schedule bigint unsigned not null,
    chosen_point int not null comment 'ѡ�λ���',
    chosen_result tinyint
(
    1
) default 1 not null comment '�γ�״̬',
    chosen_score float null comment '���ռ���',
    constraint chosen_id
    unique
(
    chosen_id
),
    constraint chosen_schedule_schedule_id_fk
    foreign key
(
    chosen_schedule
) references se_project.schedule
(
    schedule_id
),
    constraint chosen_user_User_id_fk
    foreign key
(
    chosen_student
) references se_project.user
(
    user_id
)
    );

create table if not exists se_project.comment
(
    comment_id
    int
    auto_increment
    primary
    key,
    user_id
    varchar
(
    8
) not null,
    comment_img int default 0 not null,
    comment_content text not null,
    comment_time timestamp default
(
    now
(
)) not null,
    comment_likes int default 0 not null,
    comment_replies int default 0 not null,
    comment_valid int default 0 not null,
    constraint comment_pk
    unique
(
    comment_id
),
    constraint comment_user_User_id_fk
    foreign key
(
    user_id
) references se_project.user
(
    user_id
)
    );

create table if not exists se_project.comment_img
(
    commentImg_id
    int
    auto_increment
    primary
    key,
    comment_id
    int
    not
    null,
    img_name
    text
    not
    null,
    constraint
    comment_img_comment_comment_id_fk
    foreign
    key
(
    comment_id
) references se_project.comment
(
    comment_id
)
    );

create
definer = se@`%` trigger se_project.add_img_to_comment
    after insert
    on se_project.comment_img
    for each row
begin
update comment
set comment_img = comment.comment_img + 1
where comment_id = new.comment_id;
end;

create
definer = se@`%` trigger se_project.remove_img_to_comment
    after delete
on se_project.comment_img
    for each row
begin
update comment
set comment_img = comment.comment_img - 1
where comment_id = old.comment_id;
end;

create table if not exists se_project.comment_likes
(
    id
    int
    auto_increment
    primary
    key,
    user_id
    varchar
(
    8
) not null,
    comment_id int not null,
    like_time timestamp default
(
    now
(
)) not null,
    read_condition tinyint
(
    1
) default 0 not null,
    constraint comment_likes_pk
    unique
(
    comment_id,
    user_id
),
    constraint comment_likes_comment_comment_id_fk
    foreign key
(
    comment_id
) references se_project.comment
(
    comment_id
),
    constraint comment_likes_user_User_id_fk
    foreign key
(
    user_id
) references se_project.user
(
    user_id
)
    );

create
definer = se@`%` trigger se_project.add_likes_to_comment
    after insert
    on se_project.comment_likes
    for each row
begin
update comment
set comment_likes = comment_likes + 1
where comment_id = new.comment_id;
end;

create
definer = se@`%` trigger se_project.remove_likes_to_comment
    after delete
on se_project.comment_likes
    for each row
begin
update comment
set comment_likes = comment_likes - 1
where comment_id = old.comment_id;
end;

create table if not exists se_project.permission
(
    permission_id
    bigint
    unsigned
    auto_increment
    primary
    key,
    user_id
    varchar
(
    8
) not null,
    role_id int not null,
    constraint permission_id
    unique
(
    permission_id
),
    constraint permission_id_2
    unique
(
    permission_id
),
    constraint permission_role_role_id_fk
    foreign key
(
    role_id
) references se_project.role
(
    role_id
),
    constraint permission_user_User_id_fk
    foreign key
(
    user_id
) references se_project.user
(
    user_id
)
    );

create table if not exists se_project.reply
(
    reply_id
    int
    auto_increment
    primary
    key,
    user_id
    varchar
(
    8
) not null comment '���лظ����û�',
    target_id varchar
(
    8
) not null comment '���ظ����û�',
    replied_id int default -1 not null,
    comment_id int not null comment '���ظ�������',
    reply_content text not null,
    reply_time timestamp default
(
    now
(
)) not null,
    reply_likes int default 0 not null,
    reply_valid int default 0 not null,
    reply_read tinyint
(
    1
) default 0 not null,
    constraint reply_comment_comment_id_fk
    foreign key
(
    comment_id
) references se_project.comment
(
    comment_id
),
    constraint reply_user_User_id_fk
    foreign key
(
    user_id
) references se_project.user
(
    user_id
),
    constraint reply_user_User_id_fk2
    foreign key
(
    target_id
) references se_project.user
(
    user_id
)
    );

create
definer = se@`%` trigger se_project.add_replies_to_comment
    after
update
    on se_project.reply
    for each row
begin
update comment
set comment_replies = comment.comment_replies + 1
where comment_id = new.comment_id
  and new.reply_valid = 1
  and old.reply_valid != 1;
end;

create
definer = se@`%` trigger se_project.add_replies_to_comment_admin
    after insert
    on se_project.reply
    for each row
begin
update comment
set comment_replies = comment.comment_replies + 1
where comment_id = new.comment_id
  and new.reply_valid = 1;
end;

create
definer = se@`%` trigger se_project.minus_replies_to_comment
    after
update
    on se_project.reply
    for each row
begin
update comment
set comment_replies = comment.comment_replies - 1
where comment_id = new.comment_id
  and new.reply_valid != 1
      and old.reply_valid = 1;
end;

create
definer = se@`%` trigger se_project.remove_replies_to_comment
    after delete
on se_project.reply
    for each row
begin
update comment
set comment_replies = comment.comment_replies - 1
where comment_id = old.comment_id
  and old.reply_valid = 1;
end;

create table if not exists se_project.reply_likes
(
    id
    int
    auto_increment
    primary
    key,
    user_id
    varchar
(
    8
) not null,
    reply_id int not null,
    like_time timestamp default
(
    now
(
)) not null,
    read_condition tinyint
(
    1
) default 0 not null,
    constraint reply_likes_pk
    unique
(
    user_id,
    reply_id
),
    constraint reply_like_reply_reply_id_fk
    foreign key
(
    reply_id
) references se_project.reply
(
    reply_id
),
    constraint reply_like_user_User_id_fk
    foreign key
(
    user_id
) references se_project.user
(
    user_id
)
    );

create
definer = se@`%` trigger se_project.add_likes_to_reply
    after insert
    on se_project.reply_likes
    for each row
begin
update reply
set reply_likes = reply_likes + 1
where reply_id = new.reply_id;
end;

create
definer = se@`%` trigger se_project.remove_likes_to_reply
    after delete
on se_project.reply_likes
    for each row
begin
update reply
set reply_likes = reply_likes - 1
where reply_id = old.reply_id;
end;

create
definer = se@`%` trigger se_project.update_permission_after_insert_user
    after insert
    on se_project.user
    for each row
BEGIN
insert into permission (user_id, role_id)
values (new.user_id, 2);
END;

create
definer = se@`%` trigger se_project.update_permission_before_delete_user
    before delete
on se_project.user
    for each row
BEGIN
delete
from permission
where user_id = old.user_id;
END;

create
definer = se@`%` trigger se_project.update_user_before_insert_user
    before insert
    on se_project.user
    for each row
BEGIN
    -- ����user_img
    IF
NEW.user_img IS NULL THEN
        SET NEW.user_img = CONCAT(NEW.user_id, '.jpeg');
END IF;

    -- ����user_mail
    IF
NEW.user_mail IS NULL THEN
        SET NEW.user_mail = CONCAT(NEW.User_id, '@mail.sustech.edu.cn');
END IF;

    -- ����user_major
    IF
NEW.user_major IS NULL THEN
        SET NEW.user_major = 'ͨʶͨ��';
END IF;
END;

