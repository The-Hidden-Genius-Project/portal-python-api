# End Points


### Attendances 

Get => /cohorts/<id>/attendances

Post => /cohorts/<id>/attendances/new

    {   
        admin_id, 
        student_id, 
        cohort_id, 
        notes
    }


### Users

Get => /users

Post => /users/new
    {
        email, 
        google_id, 
        role_id, 
        name
    }