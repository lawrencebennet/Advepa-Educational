from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from users.models import *
from django.contrib.auth.models import User
from itertools import groupby


class UserLoginView(APIView):
    def post(self, request):
        try:
            if request.query_params.get('token'):
                if request.query_params.get('token') == '7H@&P*9F$5m#Z!xK':
                    if request.query_params.get('username') and request.query_params.get('password'):
                        username = request.query_params.get('username')
                        password = request.query_params.get('password')
                        try:
                            user = CustomUser.objects.get(username=username)
                        except:
                            return Response({"auth_response": False, "error": "User not exist!"})
                        if user and user.check_password(password):
                            # Le credenziali di autenticazione sono corrette prosegue
                            user_dict = {
                                "username": user.username,
                                "name": user.name,
                                "last_name": user.last_name,
                                "avatar": user.avatar
                            }
                            school = user.school
                            school_dict = {}
                            if school:
                                classroom_list = [{'id': classroom.id, 'aulatype': classroom.name} for classroom in
                                                  Classroom.objects.filter(type='class', school=school)]
                                labs_list = [{'id': lab.id, 'aulatype': lab.name} for lab in
                                             Classroom.objects.filter(type='lab', school=school)]
                                school_dict = {
                                    "id_scuola": school.custom_id,
                                    "name_scuola": school.name,
                                    "tema": school.theme,
                                    "link_sportello": school.listening_desk,
                                    "modulo_ingresso": school.modulo_ingresso,
                                    "modulo_comunicazione_multipla": school.modulo_comunicazione_multipla,
                                    "modulo_personalizzato_apprendimento": school.modulo_personalizzato_apprendimento,
                                    "modulo_eventi": school.modulo_eventi,
                                    "modulo_segreteria": school.modulo_segreteria,
                                    "modulo_spazio_docenti": school.modulo_spazio_docenti,
                                    "modulo_classi_innovative": school.modulo_classi_innovative,
                                    "aule": classroom_list,
                                    "laboratori": labs_list,
                                }

                            return Response({
                                "auth_response": True,
                                "user": user_dict,
                                "school": school_dict
                            })

                    # Se le credenziali non sono corrette, ritorna False
                    return Response({"auth_response": False})
                else:
                    return Response({"Wrong authentication"})
            else:
                return Response({"Missing Token"})
        except:
            return Response({"Something went wrong!"})


class UserChangeAvatarView(APIView):
    def post(self, request):
        try:
            if request.query_params.get('token'):
                if request.query_params.get('token') == '7H@&P*9F$5m#Z!xK':
                    if request.query_params.get('username') and request.query_params.get('avatar'):
                        username = request.query_params.get('username')
                        avatar = request.query_params.get('avatar')

                        user = CustomUser.objects.get(username=username)
                        user.avatar = avatar
                        user.save()
                        return Response({"Avatar updated correctly!"})
                else:
                    return Response({"Wrong authentication"})
            else:
                return Response({"Missing Token"})
        except:
            return Response({"Something went wrong!"})


class MediaFilesClassroom(APIView):
    def post(self, request):
        try:
            if request.query_params.get('token'):
                if request.query_params.get('token') == '7H@&P*9F$5m#Z!xK':
                    if request.query_params.get('school_id') and request.query_params.get('class_id'):
                        school_id = request.query_params.get('school_id')
                        class_id = request.query_params.get('class_id')

                        # TODO chiedere alla giulia dell'id classe se vuole il numero della classe
                        classroom = Classroom.objects.get(school__custom_id=school_id, room_number=class_id)
                        if classroom:
                            mediafiles_dict = {}
                            for mediafile in classroom.media_files.all():
                                mediafiles_dict[mediafile.id] = {
                                    'type': mediafile.type.macro_type,
                                    'url': mediafile.file.path,
                                }
                            return Response(mediafiles_dict)
                    return Response({"No parameters!"})
                else:
                    return Response({"Wrong authentication"})
            else:
                return Response({"Missing Token"})
        except:
            return Response({"Something went wrong!"})


class FaqsView(APIView):
    def post(self, request):
        try:
            if request.query_params.get('token'):
                if request.query_params.get('token') == '7H@&P*9F$5m#Z!xK':
                    if request.query_params.get('school_id'):
                        school_id = request.query_params.get('school_id')
                        faq_sections = FaqSection.objects.filter(school__custom_id=school_id).order_by('area_id')
                        if faq_sections:
                            section_faqs_list = []
                            for section in faq_sections:
                                faqs_list = []
                                for faq in section.faqs:
                                    if faq.link:
                                        faqs_list.append({
                                            'question': faq.question,
                                            'answer': faq.answer,
                                            'link': faq.link
                                        })
                                    else:
                                        faqs_list.append({
                                            'question': faq.question,
                                            'answer': faq.answer
                                        })
                                section_faqs_list.append({
                                    'area_id': section.area_id,
                                    'url_avatar': section.url_avatar,
                                    'faq': faqs_list
                                })
                            return Response({'faqs': section_faqs_list})
                    return Response({"No parameters!"})
                else:
                    return Response({"Wrong authentication"})
            else:
                return Response({"Missing Token"})
        except:
            return Response({"Something went wrong!"})


class NoticesView(APIView):
    def post(self, request):
        # if request.query_params.get('token'):
        TYPE_CHOICES = {
            'news': 'news',
            'doc': 'documents',
            'meet': 'calendar'
        }
        try:
            if request.query_params.get('token'):
                if request.query_params.get('token') == '7H@&P*9F$5m#Z!xK':
                    if request.query_params.get('school_id'):
                        school_id = request.query_params.get('school_id')
                        notices = Notice.objects.filter(school__custom_id=school_id).order_by('type')
                        if notices:
                            notices_list = []  # Inizializza la lista principale fuori dal ciclo
                            for type, notice_group in groupby(notices, key=lambda notice: notice.type):
                                notice_list = list(notice_group)  # Lista di Notices per l'area corrente
                                if notice_list:
                                    notices_final_list = []  # Inizializza la lista delle Notices per l'area corrente
                                    for notice in notice_list:
                                        if type == 'news':
                                            notices_final_list.append({
                                                'title': notice.title,
                                                'data': notice.last_modify_date.date(),
                                                'text': notice.text,
                                                'link': notice.link,
                                            })
                                        elif type == 'doc':
                                            notices_final_list.append({
                                                'title': notice.title,
                                                'link': notice.media_file.file.path,
                                            })
                                        elif type == 'meet':
                                            notices_final_list.append(notice.meet_link)
                                    notices_list.append({
                                        TYPE_CHOICES[type]: notices_final_list
                                    })
                            return Response({'bacheca': notices_list})
                    return Response({"No notices!"})
                else:
                    return Response({"Wrong authentication"})
            else:
                return Response({"Missing Token"})
        except:
            return Response({"Something went wrong!"})
    # else:
    #     return Response({"Not Authorized!"})
# class SchoolSerializer(serializers.Serializer):
#     class Meta:
#         model = School
#         fields = '__all__'
# class GetSchoolDetails(APIView):
#     def get(self, request):
#         try:
#             if request.query_params.get('id'):
#                 school_id = request.query_params.get('id')
#                 school = School.objects.get(custom_id=school_id)
#                 # serializer = SchoolSerializer(school)
#                 # Modifica il dizionario della risposta JSON qui
#                 custom_data = {
#                     "id": school_id,
#                     "custom_key": "valore personalizzato",
#                     # Altri campi personalizzati
#                 }
#                 return Response(custom_data)
#         except School.DoesNotExist:
#             return Response(
#                 {"error": "Scuola non trovata"}
#             )
