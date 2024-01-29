// Script for csrf token
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.substring('csrftoken='.length, cookie.length);
        }
    }
    return '';
}

// Script edit project
$(document).ready(function() {
    function toggleEditView(projectId) {
        $(`#name-${projectId}-text`).toggleClass('d-none');
        $(`#description-${projectId}-text`).toggleClass('d-none');
        $(`#start-date-${projectId}-text`).toggleClass('d-none');
        $(`#end-date-${projectId}-text`).toggleClass('d-none');

        $(`#name-${projectId}`).toggleClass('d-none');
        $(`#description-${projectId}`).toggleClass('d-none');
        $(`#start-date-${projectId}`).toggleClass('d-none');
        $(`#end-date-${projectId}`).toggleClass('d-none');

        $(`.edit-button[data-id="${projectId}"]`).toggleClass('d-none'); 
        $(`.save-button[data-id="${projectId}"]`).toggleClass('d-none'); 
        $(`.archive-button[data-id="${projectId}"]`).toggleClass('d-none'); 
        $(`.manage-button[data-id="${projectId}"]`).toggleClass('d-none'); 
        $(`.delete-button[data-id="${projectId}"]`).toggleClass('d-none'); 
    }

    // Edit button event
    $('.edit-button').click(function() {
        const projectId = $(this).data('id');
        toggleEditView(projectId);
    });

    // Save button event
    $('.save-button button').click(function() {
        const projectId = $(this).closest('.save-button').data('id');
        const name = $(`#name-${projectId}`).val();
        const description = $(`#description-${projectId}`).val();
        const startDate = $(`#start-date-${projectId}`).val();
        const endDate = $(`#end-date-${projectId}`).val();
        
        // Update project
        $.ajax({
            url: `/update_project/${projectId}/`,
            method: 'POST',
            data: JSON.stringify({ name: name, description: description, start_date: startDate, end_date: endDate }),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val() 
            },
            success: function(data) {
                console.log(data); 
                toggleEditView(projectId); 
            },
            success: function(response) {
                if (response.message === 'Project updated successfully!') {
                    // Update DOM 
                    $(`#name-${projectId}-text`).text(name);
                    $(`#description-${projectId}-text`).text(description);
                    $(`#start-date-${projectId}-text`).text(startDate);
                    $(`#end-date-${projectId}-text`).text(endDate);

                    toggleEditView(projectId);
                } else {
                    alert('Error to update a project');
                }
            },
            error: function(error) {
                console.error(error); 
        }});
    });
});



// Script soft click secondary menu in index page
$(document).ready(function(){
    if (window.location.pathname === '/') {
        $('a[href^="#"]').on('click', function(event) {
            var target = $(this.getAttribute('href'));
            if( target.length ) {
                event.preventDefault();
                $('html, body').stop().animate({
                    scrollTop: target.offset().top - 70
                }, 1000);
            }
        });
    }
});

// Fix secondary menu in top on scroll function
var navbar = document.querySelector("#navbar");
if (navbar) {
  window.addEventListener('scroll', function() {
    if (window.scrollY > 70) { 
        navbar.classList.add('fixed-top');
        document.body.style.paddingTop = navbar.offsetHeight + 'px';
    } else {
        navbar.classList.remove('fixed-top');
        document.body.style.paddingTop = 0;
    }
  });
}


// Script for create project button
var createProjectButton = document.querySelector("#create-project-button");
if (createProjectButton) {
    createProjectButton.addEventListener("click", function() {
    document.getElementById("create-project-form").style.display = "block";
    createProjectButton.style.display = "none";
  });
}


//Script for delete project
$('.delete-button').click(function() {
    if (confirm('Are you sure you want to delete this project?')) {
        const projectId = $(this).closest('.delete-button').data('id');
        const password = prompt('Please enter your password:');
        
        if (password !== null && password.trim() !== '') {
           
            $.ajax({
                url: `/delete_project/${projectId}/`,
                type: 'DELETE',
                headers: { 'X-CSRFToken': getCSRFToken() },
                success: function(response) {
                    alert(response.message);
                    window.location.reload(); 
                },
                error: function(xhr, status, error) {
                    alert('Error deleting the project');
                    console.error(error);
                }
            });
        } else {
            alert('Password is required.');
        }
    }
});

// Script archive project
$(document).ready(function() {
    $('.archive-button').click(function(event) {
        event.preventDefault();
        const projectId = $(this).data('id');
        const confirmArchive = confirm("Are you sure you want to archive this project?");

        if (confirmArchive) {
            const csrftoken = getCSRFToken();

            $.ajax({
                type: 'POST',
                url: `/archive_project/${projectId}/`,
                data: {
                    csrfmiddlewaretoken: csrftoken
                },
                success: function(response) {
                    console.log(response);
                    location.reload();
                },
                error: function(xhr, status, error) {
                    console.error(xhr.responseText);
                }
            });
        }
    });
});

// Script unarchive project
$(document).ready(function() {
    $('.unarchive-button').click(function(event) {
        event.preventDefault();
        const projectId = $(this).data('id');
        const confirmUnarchive = confirm("Are you sure you want to unarchive this project?");

        if (confirmUnarchive) {
            const csrftoken = getCSRFToken();

            $.ajax({
                type: 'POST',
                url: `/unarchive_project/${projectId}/`, 
                data: {
                    csrfmiddlewaretoken: csrftoken
                },
                success: function(response) {
                    console.log(response);
                    location.reload(); 
                },
                error: function(xhr, status, error) {
                    console.error(xhr.responseText);
                }
            });
        }
    });
});

