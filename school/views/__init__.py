from .index import index
from .login_register import login, logout, register, ajax_get_identify_number_from_sms, ajax_get_verify_code_image
from .account import account_list
from .teacher import teacher_list, teacher_detail, teacher_create, teacher_update, teacher_delete
from .student import student_list, student_delete, student_create, student_update, student_detail
from .course import course_list, course_detail, course_create, course_update, course_delete
