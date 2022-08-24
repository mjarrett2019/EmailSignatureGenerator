function generate_signature() {
    let email = document.getElementsByClassName("input--style-2").innerHTML
    let pronouns = document.getElementsByClassName("rs-select2 js-select-simple select--no-search").innerHTML
    let signature = "<b>Matt JARRETT</b> | " + pronouns + " | Deskside Technician | LV Headoffice\n1 East 57th Street New York, NY 10022 | Mobile: (248)303-9989 | " + email
    document.getElementsByClassName("card-body").innerHTML = signature
}