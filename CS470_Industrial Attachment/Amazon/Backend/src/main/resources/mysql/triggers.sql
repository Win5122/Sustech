#
�û�����
-- ����userǰ���г�ʼ��
create
definer = se@`%` trigger if not exists update_user_before_insert_user
    before insert
    on user
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
-- �����û������permission
create
definer = se@`%` trigger if not exists update_permission_after_insert_user
    after insert
    on user
    for each row
BEGIN
insert into permission (user_id, role_id)
values (new.user_id, 2);
END;
-- ɾ���û�ǰ����permission
create
definer = se@`%` trigger if not exists update_permission_before_delete_user
    before delete
on user
    for each row
BEGIN
delete
from permission
where user_id = old.user_id;
END;

#
�γ̲���
## רҵ����
-- ɾ��majorǰ����ȫ��major����
create
definer = se@`%` trigger if not exists update_user_before_delete_major
    before delete
on major
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
##
�α���
-- ����scheduleǰ���г�ʼ��
create
definer = se@`%` trigger if not exists update_schedule_before_insert_schedule
    before insert
    on schedule
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
##
ѡ�β���
-- ����ѡ�κ����schedule_have
create
definer = se@`%` trigger if not exists add_schedule_have_after_insert_chosen
    after insert
    on chosen
    for each row
begin
update schedule
set schedule_have = schedule.schedule_have + 1
where schedule_id = new.chosen_schedule;
end;
-- ���ѡ��ǰ����schedule_have
create
definer = se@`%` trigger if not exists minus_schedule_have_before_delete_chosen
    before delete
on chosen
    for each row
begin
update schedule
set schedule_have = schedule.schedule_have - 1
where schedule_id = old.chosen_schedule;
end;
##
���㲿��
-- ����chosen�����ѧ������
create
definer = se@`%` trigger if not exists update_user_after_insert_chosen
    after insert
    on chosen
    for each row
BEGIN
    IF
NEW.chosen_score IS NOT NULL THEN
        with userScore as (select sum(course_score * chosen_score) / sum(course_score) as userScore
                           from chosen
                                    left join schedule on chosen.chosen_schedule = schedule.schedule_id
                                    left join course on schedule.schedule_course = course.course_id
                           where chosen.chosen_student = new.chosen_student
                             and chosen.chosen_result != 0
                             and chosen.chosen_score is not null)
UPDATE user
set user_score = IF((select userScore from userScore) is null, 0, (select userScore from userScore))
where user_id = new.chosen_student;
end if;
END;
-- ����ѧ�Ƽ�������ѧ������
create
definer = se@`%` trigger if not exists update_user_after_update_chosen
    after
update
    on chosen
    for each row
BEGIN
    IF
(old.chosen_score != new.chosen_score OR OLD.chosen_score IS NULL OR NEW.chosen_score IS NULL)
        OR (OLD.chosen_result != NEW.chosen_result)
    THEN
        with userScore as (select sum(course_score * chosen_score) / sum(course_score) as userScore
                           from chosen
                                    left join schedule on chosen.chosen_schedule = schedule.schedule_id
                                    left join course on schedule.schedule_course = course.course_id
                           where chosen.chosen_student = old.chosen_student
                             and chosen.chosen_result != 0
                             and chosen.chosen_score is not null)
UPDATE user
set user_score = IF((select userScore from userScore) is null, 0, (select userScore from userScore))
where user_id = old.chosen_student;
end if;
END;
-- �h��chosenǰ���W�����c
create
definer = se@`%` trigger if not exists update_user_before_delete_chosen
    after delete
on chosen
    for each row
BEGIN
    IF
old.chosen_result != 0 THEN
        with userScore as (select sum(course_score * chosen_score) / sum(course_score) as userScore
                           from chosen
                                    left join schedule on chosen.chosen_schedule = schedule.schedule_id
                                    left join course on schedule.schedule_course = course.course_id
                           where chosen.chosen_student = old.chosen_student
                             and chosen.chosen_result != 0
                             and chosen.chosen_score is not null)
UPDATE user
set user_score = IF((select userScore from userScore) is null, 0, (select userScore from userScore))
where user_id = old.chosen_student;
end if;
END;

#
��̳����
## ����ɾ��
-- ����Ա���һ���ظ�
create
definer = se@`%` trigger if not exists add_replies_to_comment_admin
    after insert
    on reply
    for each row
begin
update comment
set comment_replies = comment.comment_replies + 1
where comment_id = new.comment_id
  and new.reply_valid = 1;
end;
-- ͨ��һ���ظ�
create
definer = se@`%` trigger if not exists add_replies_to_comment
    after
update
    on reply
    for each row
begin
update comment
set comment_replies = comment.comment_replies + 1
where comment_id = new.comment_id
  and new.reply_valid = 1
  and old.reply_valid != 1;
end;
-- �¼�һ���ظ�
create
definer = se@`%` trigger if not exists minus_replies_to_comment
    after
update
    on reply
    for each row
begin
update comment
set comment_replies = comment.comment_replies - 1
where comment_id = new.comment_id
  and new.reply_valid != 1
      and old.reply_valid = 1;
end;
-- ɾ��һ���ظ�
create
definer = se@`%` trigger if not exists remove_replies_to_comment
    after delete
on reply
    for each row
begin
update comment
set comment_replies = comment.comment_replies - 1
where comment_id = old.comment_id
  and old.reply_valid = 1;
end;
#-- ����
-- �����۵���
create
definer = se@`%` trigger if not exists add_likes_to_comment
    after insert
    on comment_likes
    for each row
begin
update comment
set comment_likes = comment_likes + 1
where comment_id = new.comment_id;
end;
-- ȡ�������۵ĵ���
create
definer = se@`%` trigger if not exists remove_likes_to_comment
    after delete
on comment_likes
    for each row
begin
update comment
set comment_likes = comment_likes - 1
where comment_id = old.comment_id;
end;
-- ���ظ�����
create
definer = se@`%` trigger if not exists add_likes_to_reply
    after insert
    on reply_likes
    for each row
begin
update reply
set reply_likes = reply_likes + 1
where reply_id = new.reply_id;
end;
-- ȡ���Իظ��ĵ���
create
definer = se@`%` trigger if not exists remove_likes_to_reply
    after delete
on reply_likes
    for each row
begin
update reply
set reply_likes = reply_likes - 1
where reply_id = old.reply_id;
end;
##
��Ƭ
-- ���������Ƭ
create
definer = se@`%` trigger if not exists add_img_to_comment
    after insert
    on comment_img
    for each row
begin
update comment
set comment_img = comment.comment_img + 1
where comment_id = new.comment_id;
end;
-- ɾ��������Ƭ
create
definer = se@`%` trigger if not exists remove_img_to_comment
    after delete
on comment_img
    for each row
begin
update comment
set comment_img = comment.comment_img - 1
where comment_id = old.comment_id;
end;

show
triggers;
