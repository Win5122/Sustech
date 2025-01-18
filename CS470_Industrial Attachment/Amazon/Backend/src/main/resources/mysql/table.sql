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
) not null comment '性质（必修/选修）',
    course_type varchar
(
    20
) not null comment '类别（通识必修、通识选修、专业核心等）',
    course_language varchar
(
    2
) not null comment '（汉语、英语、双语）',
    course_count varchar
(
    20
) not null comment '计分方式',
    course_score int default 0 not null comment '学分',
    course_last int not null comment '学时',
    course_major varchar
(
    20
) default '通识通修' not null,
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
    -- 更新user_major
update user
set user_major = '通识通修'
where user_major = old.major_name;
-- 更新teacher_major
update teacher
set teacher_major = '通识通修'
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
) null comment '职称（教授、副教授等）',
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
) not null comment '学年学期',
    schedule_course varchar
(
    20
) not null,
    schedule_class int not null comment '班级',
    schedule_group int null comment '小组',
    schedule_teacher1 varchar
(
    20
) not null,
    schedule_week1 varchar
(
    10
) not null comment '单双周等情况',
    schedule_time1 varchar
(
    11
) not null comment '时间 e.g. 08:00-09:50',
    schedule_place1 varchar
(
    20
) not null comment '地点',
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
    schedule_total int not null comment '容量',
    schedule_have int default 0 not null comment '已选',
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
    -- 更新schedule_term
    IF
NEW.schedule_term IS NULL THEN
        SET NEW.schedule_term = CONCAT(YEAR(NOW()),
                                       case
                                           when month(NOW()) in (2, 3, 4, 5, 6) then '春季'
                                           when month(NOW()) in (7, 8) then '夏季'
                                           when month(NOW()) in (9, 10, 11, 12, 1) then '秋季'
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
) default '通识通修' not null,
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
    chosen_point int not null comment '选课积分',
    chosen_result tinyint
(
    1
) default 1 not null comment '课程状态',
    chosen_score float null comment '最终绩点',
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
) not null comment '进行回复的用户',
    target_id varchar
(
    8
) not null comment '被回复的用户',
    replied_id int default -1 not null,
    comment_id int not null comment '被回复的评论',
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
    -- 更新user_img
    IF
NEW.user_img IS NULL THEN
        SET NEW.user_img = CONCAT(NEW.user_id, '.jpeg');
END IF;

    -- 更新user_mail
    IF
NEW.user_mail IS NULL THEN
        SET NEW.user_mail = CONCAT(NEW.User_id, '@mail.sustech.edu.cn');
END IF;

    -- 更新user_major
    IF
NEW.user_major IS NULL THEN
        SET NEW.user_major = '通识通修';
END IF;
END;

