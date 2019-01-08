from django import template
register = template.Library()

from contact.models import ContactAdminStatus, ContactExpertStatus

from django.utils.safestring import mark_safe


@register.simple_tag
def get_status_list(contact_id, value):
    str_to_return = '<select name="status" id="id_status" class="select form-control">'
    for status in ContactAdminStatus.objects.all():
        if str(value) == str(status.title):
            str_to_return += '<option selected value="{}">{}</option>'.format(status.id, status.title)
        else:
            str_to_return += '<option value="{}">{}</option>'.format(status.id, status.title)
    str_to_return += '</select>'
    str_to_return += '<script type="text/javascript">'
    str_to_return += """
                     function defer(method) {
                        if (window.jQuery) {
                            method();
                        } else {
                            setTimeout(function() { defer(method) }, 50);
                        }
                    }
                    defer(function () {
                      
                       $("#id_status").change( function() {
                           $(this).find(":selected").each(function () {
                                    var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
                                    function csrfSafeMethod(method) {
                                    // these HTTP methods do not require CSRF protection
                                        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                                    }
                                    $.ajaxSetup({
                                        beforeSend: function(xhr, settings) {
                                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                            }
                                        }
                                    });
                                    $.post('/admin-area/contact/change-status/', 
                                    { 'status_pk': $(this).val(), 'contact_admin_pk' : %s }, 
                                            function(returnedData){
                                                 console.log(returnedData);
                                        });
                            });
                         });
                        
                    })
                    """ % (contact_id,)
    str_to_return += '</script>'

    return mark_safe(str_to_return)


@register.simple_tag
def get_expert_status_list(contact_id, value):
    str_to_return = '<select name="status" id="id_status" class="select form-control">'
    for status in ContactExpertStatus.objects.all():
        if str(value) == str(status.title):
            str_to_return += '<option selected value="{}">{}</option>'.format(status.id, status.title)
        else:
            str_to_return += '<option value="{}">{}</option>'.format(status.id, status.title)
    str_to_return += '</select>'
    str_to_return += '<script type="text/javascript">'
    str_to_return += """
                     function defer(method) {
                        if (window.jQuery) {
                            method();
                        } else {
                            setTimeout(function() { defer(method) }, 50);
                        }
                    }
                    defer(function () {

                       $("#id_status").change( function() {
                           $(this).find(":selected").each(function () {
                                    var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
                                    function csrfSafeMethod(method) {
                                    // these HTTP methods do not require CSRF protection
                                        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                                    }
                                    $.ajaxSetup({
                                        beforeSend: function(xhr, settings) {
                                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                            }
                                        }
                                    });
                                    $.post('/admin-area/contact-expert/change-status/', 
                                    { 'status_pk': $(this).val(), 'contact_admin_pk' : %s }, 
                                            function(returnedData){
                                                 console.log(returnedData);
                                        });
                            });
                         });

                    })
                    """ % (contact_id,)
    str_to_return += '</script>'

    return mark_safe(str_to_return)
