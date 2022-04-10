const bodyweight = document.getElementById('bodyweight');
const age = document.getElementById('age');
const squat = document.getElementById('squat');
const bench = document.getElementById('bench');
const deadlift = document.getElementById('deadlift');
const submit_button = document.getElementById('submit_button');
const errorElement = document.getElementById('error');




submit_button.addEventListener('click', e => {
    let empty_fields = [];

    if (bodyweight.value == '') {
        empty_fields.push('Bodyweight');
    }

    if (age.value == '') {
        empty_fields.push('Age');
    }

    if (squat.value == '') {
        empty_fields.push('Squat');
    }

    if (bench.value == '') {
        empty_fields.push('Bench');
    }

    if (deadlift.value == '') {
        empty_fields.push('Deadlift');
    }

    //can't calculate results without all fields filled in
    if (empty_fields.length > 0) {
        e.preventDefault(); 
        errorElement.innerText = 'The following fields are required: '.concat(empty_fields.join(', '));
    }
    
})