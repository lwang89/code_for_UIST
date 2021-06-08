<template>
    <div class="card">
        <h3 class="card-header text-center">Subject Information for ID: {{subject_id}}</h3>
        <div class="card-body">
            <form @submit.prevent="submit">
                <ol>

                    <!-- Radio -->
                    <!-- Return: Gender -->
                    <div class="form-group">
                        <li><label id="gender">Gender</label></li>

                        <input type="radio" id="gender_male" value="male" v-model="$v.result.gender.$model" :class="{'is-invalid': $v.result.gender.$error, 'is-valid': !$v.result.gender.$invalid}">
                        <label for="gender_male">Male</label>
                        <br/>

                        <input type="radio" id="gender_female" value="female" v-model="$v.result.gender.$model" :class="{'is-invalid': $v.result.gender.$error, 'is-valid': !$v.result.gender.$invalid}">
                        <label for="gender_female">Female</label>
                        <br/>

                        <input type="radio" id="gender_trans_male" value="trans_male" v-model="$v.result.gender.$model" :class="{'is-invalid': $v.result.gender.$error, 'is-valid': !$v.result.gender.$invalid}">
                        <label for="gender_trans_male">Transgender Male/Transman/FTM</label>
                        <br/>
                        
                        <input type="radio" id="gender_trans_female" value="trans_female" v-model="$v.result.gender.$model" :class="{'is-invalid': $v.result.gender.$error, 'is-valid': !$v.result.gender.$invalid}">
                        <label for="gender_trans_female">Transgender Female/Transwoman/MTF</label>
                        <br/>

                        <input type="radio" id="gender_queer" value="gender_queer" v-model="$v.result.gender.$model" :class="{'is-invalid': $v.result.gender.$error, 'is-valid': !$v.result.gender.$invalid}">
                        <label for="gender_queer">Gender Queer</label>
                        <br/>

                        <input type="radio" id="gender_additional" value="additional_category" v-model="$v.result.gender.$model" :class="{'is-invalid': $v.result.gender.$error, 'is-valid': !$v.result.gender.$invalid}">
                        <label for="gender_additional">Additional category</label>
                        <br/>

                        <input type="radio" id="gender_decline" value="decline_to_answer" v-model="$v.result.gender.$model" :class="{'is-invalid': $v.result.gender.$error, 'is-valid': !$v.result.gender.$invalid}">
                        <label for="gender_decline">Decline to answer</label>
                        
                        <div class="invalid-feedback">
                            <span v-if="!$v.result.gender.required">Please select your answer.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Radio -->
                    <!-- Return: Sex at birth -->
                    <div class="form-group">
                        <li><label id="gender">What sex were you assigned at birth?</label></li>

                        <input type="radio" id="sex_birth_male" value="male" v-model="$v.result.sex_at_birth.$model" :class="{'is-invalid': $v.result.sex_at_birth.$error, 'is-valid': !$v.result.sex_at_birth.$invalid}">
                        <label for="sex_birth_male">Male</label>
                        <br/>

                        <input type="radio" id="sex_birth_female" value="female" v-model="$v.result.sex_at_birth.$model" :class="{'is-invalid': $v.result.sex_at_birth.$error, 'is-valid': !$v.result.sex_at_birth.$invalid}">
                        <label for="sex_birth_female">Female</label>
                        <br/>
                        
                        <input type="radio" id="sex_birth_other" value="other" v-model="$v.result.sex_at_birth.$model" :class="{'is-invalid': $v.result.sex_at_birth.$error, 'is-valid': !$v.result.sex_at_birth.$invalid}">
                        <label for="sex_birth_other">Other</label>
                        <br/>

                        
                        <input type="radio" id="sex_birth_decline" value="decline_to_answer" v-model="$v.result.sex_at_birth.$model" :class="{'is-invalid': $v.result.sex_at_birth.$error, 'is-valid': !$v.result.sex_at_birth.$invalid}">
                        <label for="sex_birth_decline">Decline to answer</label>
                        
                        <div class="invalid-feedback">
                            <span v-if="!$v.result.sex_at_birth.required">Please select your answer.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Number -->
                    <!-- Return: Age -->
                    <div class="form-group">
                        <li><label id="age">Age</label></li>

                        <input type="number" class="form-control" v-model.number="$v.result.age.$model" :class="{'is-invalid': $v.result.age.$error, 'is-valid': !$v.result.age.$invalid}">

                        <div class="valid-feedback">Your age is valid!</div>
                        <div class="invalid-feedback">
                            <span v-if="!$v.result.age.required">Please input a number.</span>
                            <span v-if="!$v.result.age.between">The age should be between {{$v.result.age.$params.between.min}} and {{$v.result.age.$params.between.max}}.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Radio -->
                    <!-- Return: Left handed in the family -->
                    <div class="form-group">
                        <li><label id="left_hand_in_family">Do you have any left-handed in the family?</label></li>

                        <input type="radio" id="left_hand_in_family_yes" value="yes" v-model="$v.result.left_hand_in_family.$model" :class="{'is-invalid': $v.result.left_hand_in_family.$error, 'is-valid': !$v.result.left_hand_in_family.$invalid}">
                        <label for="left_hand_in_family_yes">Yes</label>
                        
                        <input type="radio" id="left_hand_in_family_no" value="no" v-model="$v.result.left_hand_in_family.$model" :class="{'is-invalid': $v.result.left_hand_in_family.$error, 'is-valid': !$v.result.left_hand_in_family.$invalid}">
                        <label for="left_hand_in_family_no">No</label>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.left_hand_in_family.required">Please select your answer.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Radio -->
                    <!-- Return: Handedness -->
                    <div class="form-group">
                        <li><label id="handedness">Which handedness do you consider yourself?</label></li>

                        <input type="radio" id="handedness_left" value="left" v-model="$v.result.handedness.$model" :class="{'is-invalid': $v.result.handedness.$error, 'is-valid': !$v.result.handedness.$invalid}">
                        <label for="handedness_left">Left-handed</label>
                        
                        <input type="radio" id="handedness_right" value="right" v-model="$v.result.handedness.$model" :class="{'is-invalid': $v.result.handedness.$error, 'is-valid': !$v.result.handedness.$invalid}">
                        <label for="handedness_right">Right-handed</label>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.handedness.required">Please select your answer.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Radio -->
                    <!-- Return: Changed handedness -->
                    <div class="form-group">
                        <li><label id="changed_handedness">Have you ever changed handedness?</label></li>

                        <input type="radio" id="change_handedness_yes" value="yes" v-model="$v.result.changed_handedness.$model" :class="{'is-invalid': $v.result.changed_handedness.$error, 'is-valid': !$v.result.changed_handedness.$invalid}">
                        <label for="change_handedness_yes">Yes</label>
                        
                        <input type="radio" id="change_handedness_no" value="no" v-model="$v.result.changed_handedness.$model" :class="{'is-invalid': $v.result.changed_handedness.$error, 'is-valid': !$v.result.changed_handedness.$invalid}">
                        <label for="change_handedness_no">No</label>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.changed_handedness.required">Please select your answer.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Radio -->
                    <!-- Return: Learning or reading disability -->
                    <div class="form-group">
                        <li><label id="learning_reading_disability">Do you have a learning or reading disability?</label></li>

                        <input type="radio" id="disability_yes" value="yes" v-model="$v.result.learning_reading_disability.$model" :class="{'is-invalid': $v.result.learning_reading_disability.$error, 'is-valid': !$v.result.learning_reading_disability.$invalid}">
                        <label for="disability_yes">Yes</label>
                        
                        <input type="radio" id="disability_no" value="no" v-model="$v.result.learning_reading_disability.$model" :class="{'is-invalid': $v.result.learning_reading_disability.$error, 'is-valid': !$v.result.learning_reading_disability.$invalid}">
                        <label for="disability_no">No</label>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.learning_reading_disability.required">Please select your answer.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Radio -->
                    <!-- Return: Is English first language -->
                    <div class="form-group">
                        <li><label id="english_first_language">Is English your first language?</label></li>

                        <input type="radio" id="first_language_yes" value="yes" v-model="$v.result.english_first_language.$model" :class="{'is-invalid': $v.result.english_first_language.$error, 'is-valid': !$v.result.english_first_language.$invalid}">
                        <label for="first_language_yes">Yes</label>
                        
                        <input type="radio" id="first_language_no" value="no" v-model="$v.result.english_first_language.$model" :class="{'is-invalid': $v.result.english_first_language.$error, 'is-valid': !$v.result.english_first_language.$invalid}">
                        <label for="first_language_no">No</label>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.english_first_language.required">Please select your answer.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Radio -->
                    <!-- Return: Head injury -->
                    <div class="form-group">
                        <li><label id="head_injury">Have you ever had a traumatic head injury?</label></li>

                        <input type="radio" id="head_injury_yes" value="yes" v-model="$v.result.head_injury.$model" :class="{'is-invalid': $v.result.head_injury.$error, 'is-valid': !$v.result.head_injury.$invalid}">
                        <label for="head_injury_yes">Yes</label>
                        
                        <input type="radio" id="head_injury_no" value="no" v-model="$v.result.head_injury.$model" :class="{'is-invalid': $v.result.head_injury.$error, 'is-valid': !$v.result.head_injury.$invalid}">
                        <label for="head_injury_no">No</label>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.head_injury.required">Please select your answer.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Radio -->
                    <!-- Return: Vision -->
                    <div class="form-group">
                        <li><label id="vision">Do you have normal or correct-to-normal vision?</label></li>

                        <input type="radio" id="vision_normal" value="normal" v-model="$v.result.vision.$model" :class="{'is-invalid': $v.result.vision.$error, 'is-valid': !$v.result.vision.$invalid}">
                        <label for="vision_normal">Normal vision</label>
                        
                        <input type="radio" id="vision_corrected" value="corrected" v-model="$v.result.vision.$model" :class="{'is-invalid': $v.result.vision.$error, 'is-valid': !$v.result.vision.$invalid}">
                        <label for="vision_corrected">Corrected-to-normal vision</label>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.vision.required">Please select your answer.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Radio -->
                    <!-- Return: Caffeine -->
                    <div class="form-group">

                        <li><label id="caffeine">Did you take anything with caffeine in the past 24 hours?</label></li>

                        <input type="radio" id="caffeine_yes" value="yes" v-model="$v.result.caffeine.$model" :class="{'is-invalid': $v.result.caffeine.$error, 'is-valid': !$v.result.caffeine.$invalid}">
                        <label for="caffeine_yes">Yes</label>
                        
                        <input type="radio" id="caffeine_no" value="no" v-model="$v.result.caffeine.$model" :class="{'is-invalid': $v.result.caffeine.$error, 'is-valid': !$v.result.caffeine.$invalid}">
                        <label for="caffeine_no">No</label>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.caffeine.required">Please select your answer.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Number -->
                    <!-- Return: Sleep Last Night -->
                    <div class="form-group">
                        <li><label id="sleep_last_night">About how many hours of sleep did you get last night?</label></li>

                        <input type="number" class="form-control" v-model.number="$v.result.sleep_last_night.$model" :class="{'is-invalid': $v.result.sleep_last_night.$error, 'is-valid': !$v.result.sleep_last_night.$invalid}">

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.sleep_last_night.required">Please input a number.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Number -->
                    <!-- Return: Sleep Ususally -->
                    <div class="form-group">
                        <li><label id="sleep_usually">About how many hours of sleep do you usually get?</label></li>

                        <input type="number" class="form-control" v-model.number="$v.result.sleep_usually.$model" :class="{'is-invalid': $v.result.sleep_usually.$error, 'is-valid': !$v.result.sleep_usually.$invalid}">

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.sleep_usually.required">Please input a number.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Radio -->
                    <!-- Return: Worn Biological Sensors -->
                    <div class="form-group">
                        <li><label id="worn_biological_sensors">Have you ever worn biological sensors (EEG, fNIRS, GSR)?</label></li>

                        <input type="radio" id="worn_biological_sensors_yes" value="yes" v-model="$v.result.worn_biological_sensors.$model" :class="{'is-invalid': $v.result.worn_biological_sensors.$error, 'is-valid': !$v.result.worn_biological_sensors.$invalid}">
                        <label for="worn_biological_sensors_yes">Yes</label>
                        
                        <input type="radio" id="worn_biological_sensors_no" value="no" v-model="$v.result.worn_biological_sensors.$model" :class="{'is-invalid': $v.result.worn_biological_sensors.$error, 'is-valid': !$v.result.worn_biological_sensors.$invalid}">
                        <label for="worn_biological_sensors_no">No</label>

                        <input type="radio" id="worn_biological_sensors_not_sure" value="not_sure" v-model="$v.result.worn_biological_sensors.$model" :class="{'is-invalid': $v.result.worn_biological_sensors.$error, 'is-valid': !$v.result.worn_biological_sensors.$invalid}">
                        <label for="worn_biological_sensors_not_sure">Not sure</label>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.worn_biological_sensors.required">Please select your answer.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Radio -->
                    <!-- Return: Experiment In Lab Environment Before -->
                    <div class="form-group">
                        <li><label id="experiment_lab_environment">Have you ever participated in an experiment in a lab environment before today?</label></li>

                        <input type="radio" id="experiment_lab_environment_yes" value="yes" v-model="$v.result.experiment_lab_environment.$model" :class="{'is-invalid': $v.result.experiment_lab_environment.$error, 'is-valid': !$v.result.experiment_lab_environment.$invalid}">
                        <label for="experiment_lab_environment_yes">Yes</label>
                        
                        <input type="radio" id="experiment_lab_environment_no" value="no" v-model="$v.result.experiment_lab_environment.$model" :class="{'is-invalid': $v.result.experiment_lab_environment.$error, 'is-valid': !$v.result.experiment_lab_environment.$invalid}">
                        <label for="experiment_lab_environment_no">No</label>

                        <input type="radio" id="experiment_lab_environment_not_sure" value="not_sure" v-model="$v.result.experiment_lab_environment.$model" :class="{'is-invalid': $v.result.experiment_lab_environment.$error, 'is-valid': !$v.result.experiment_lab_environment.$invalid}">
                        <label for="experiment_lab_environment_not_sure">Not sure</label>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.experiment_lab_environment.required">Please select your answer.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Radio -->
                    <!-- Return: N-back Experience -->
                    <div class="form-group">
                        <li><label id="n_back_knowledge">Have you completed an n-back task before?</label></li>

                        <input type="radio" id="n_back_knowledge_yes" value="yes" v-model="$v.result.n_back_knowledge.$model" :class="{'is-invalid': $v.result.n_back_knowledge.$error, 'is-valid': !$v.result.n_back_knowledge.$invalid}">
                        <label for="n_back_knowledge_yes">Yes</label>
                        
                        <input type="radio" id="n_back_knowledge_no" value="no" v-model="$v.result.n_back_knowledge.$model" :class="{'is-invalid': $v.result.n_back_knowledge.$error, 'is-valid': !$v.result.n_back_knowledge.$invalid}">
                        <label for="n_back_knowledge_no">No</label>

                        <input type="radio" id="n_back_knowledge_not_sure" value="not_sure" v-model="$v.result.n_back_knowledge.$model" :class="{'is-invalid': $v.result.n_back_knowledge.$error, 'is-valid': !$v.result.n_back_knowledge.$invalid}">
                        <label for="n_back_knowledge_not_sure">Not sure</label>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.n_back_knowledge.required">Please select your answer.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Radio -->
                    <!-- Return: Prescription Drug -->
                    <div class="form-group">
                        <li><label id="prescription_drug">Have you used any prescription drug in the past 30 days?</label></li>

                        <input type="radio" id="prescription_drug_yes" value="yes" v-model="$v.result.prescription_drug.$model" :class="{'is-invalid': $v.result.prescription_drug.$error, 'is-valid': !$v.result.prescription_drug.$invalid}">
                        <label for="prescription_drug_yes">Yes</label>
                        
                        <input type="radio" id="prescription_drug_no" value="no" v-model="$v.result.prescription_drug.$model" :class="{'is-invalid': $v.result.prescription_drug.$error, 'is-valid': !$v.result.prescription_drug.$invalid}">
                        <label for="prescription_drug_no">No</label>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.prescription_drug.required">Please select your answer.</span>
                        </div>
                    </div>

                    <div v-if="result.prescription_drug==='yes'">
                        <hr />

                        <div class="form-group">
                            <!-- text -->
                            <!-- Return: Prescription Drug Last time-->
                            <li><label>What's the last time of taking the prescription drug? What's the drug?</label></li>
                            <textarea type="text" placeholder="please input text" class="form-control input" v-model.trim="result.prescription_drug_last_time"></textarea>
                        </div>
                    </div>

                    <hr />

                    <!-- Radio -->
                    <!-- Return: Recreational Drug -->
                    <div class="form-group">
                        <li><label id="vision">Have you used any recreational drug in the past 30 days?</label></li>

                        <input type="radio" id="recreational_drug_yes" value="yes" v-model="$v.result.recreational_drug.$model" :class="{'is-invalid': $v.result.recreational_drug.$error, 'is-valid': !$v.result.recreational_drug.$invalid}">
                        <label for="recreational_drug_yes">Yes</label>
                        
                        <input type="radio" id="recreational_drug_no" value="no" v-model="$v.result.recreational_drug.$model" :class="{'is-invalid': $v.result.recreational_drug.$error, 'is-valid': !$v.result.recreational_drug.$invalid}">
                        <label for="recreational_drug_no">No</label>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.recreational_drug.required">Please select your answer.</span>
                        </div>
                    </div>

                    <div v-if="result.recreational_drug==='yes'" class="form-group">
                        <hr />

                        <div class="form-group">
                            <!-- text -->
                            <!-- Return: Recreational Drug Last time-->
                            <li><label>What's the last time of taking the recreational drug? What's the drug?</label></li>
                            <textarea type="text" placeholder="please input text" class="form-control input" v-model.trim="result.recreational_drug_last_time"></textarea>
                        </div>
                    </div>

                    <hr />

                    <!-- Checkbox -->
                    <!-- Return: Ethnicity -->
                    <div class="form-group">
                        <li><label id="vision">How would you describe yourself? (Check all that apply)</label></li>

                        <input type="checkbox" id="ethnicity_american_native" value="American Indian or Alaska Native" v-model="result.ethnicity">
                        <label for="ethnicity_american_native">American Indian or Alaska Native</label>
                        <br/>
                        <input type="checkbox" id="ethnicity_asian" value="Asian" v-model="result.ethnicity">
                        <label for="ethnicity_asian">Asian</label>
                        <br/>
                        <input type="checkbox" id="ethnicity_black_african" value="Black or African American" v-model="result.ethnicity">
                        <label for="ethnicity_black_african">Black or African American</label>
                        <br/>
                        <input type="checkbox" id="ethnicity_hawaiian_pacific" value="Native Hawaiian or Other Pacific Islander" v-model="result.ethnicity">
                        <label for="ethnicity_hawaiian_pacific">Native Hawaiian or Other Pacific Islander</label>
                        <br/>
                        <input type="checkbox" id="ethnicity_white" value="White" v-model="result.ethnicity">
                        <label for="ethnicity_white">White</label>
                        <br/>
                        <input type="checkbox" id="ethnicity_hispanic_latino" value="Hispanic or Latino or Spanish Origin" v-model="result.ethnicity">
                        <label for="ethnicity_hispanic_latino">Hispanic or Latino or Spanish Origin</label>
                        <br/>
                        <input type="checkbox" id="ethnicity_not_hispanic" value="Not Hispanic or Latino or Spanish Origin" v-model="result.ethnicity">
                        <label for="ethnicity_not_hispanic">Not Hispanic or Latino or Spanish Origin</label>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.ethnicity.required">Please select your answer.</span>
                        </div>
                    </div>

                </ol>
                <p class="typo__p" v-if="submitStatus === 'ERROR'">Please fill the form correctly.</p>
            </form>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { required, between } from 'vuelidate/lib/validators';

export default {
    name: "SubjectInformation",

    data() {
        return {
            next: {name: "general_intro"},
            subject_id                          : "default id",
            result: {
                gender                          : "",   // Radio: male/female/trans_male/trans_female/gender_queer/additional_category/decline_to_answer
                sex_at_birth                    : "",   // Radio: male/female/other/decline_to_answer
                age                             : "",   // Number
                left_hand_in_family             : "",   // Radio: yes/no
                handedness                      : "",   // Radio: left/right
                changed_handedness              : "",   // Radio: yes/no
                learning_reading_disability     : "",   // Radio: yes/no
                english_first_language          : "",   // Radio: yes/no
                head_injury                     : "",   // Radio: yes/no
                vision                          : "",   // Radio: normal/corrected
                caffeine                        : "",   // Radio: yes/no
                sleep_usually                   : "",   // Number
                sleep_last_night                : "",   // Number
                worn_biological_sensors         : "",   // Radio: yes/no/not_sure
                experiment_lab_environment      : "",   // Radio: yes/no/not_sure
                n_back_knowledge                : "",   // Radio: yes/no
                prescription_drug               : "",   // Radio: yes/no
                prescription_drug_last_time     : "",   // Text
                recreational_drug               : "",   // Radio: yes/no
                recreational_drug_last_time     : "",   // Text
                ethnicity                       : []    // Checkbox: "American Indian or Alaska Native","Asian","Black or African American","Native Hawaiian or Other Pacific Islander","White","Hispanic or Latino or Spanish Origin","Not Hispanic or Latino or Spanish Origin"
            },
            submitStatus: null,
        };
    },

    mounted() {
        this.getSubjectID();
    },

    validations: {
        result:{
            gender: {
                required,
            },
            sex_at_birth: {
                required,
            },
            age: {
                required,
                between: between(10, 70)
            },
            left_hand_in_family: {
                required,
            },
            handedness: {
                required,
            },
            changed_handedness: {
                required,
            },
            learning_reading_disability: {
                required,
            },
            english_first_language: {
                required,
            },
            head_injury: {
                required,
            },
            vision: {
                required,
            },
            caffeine: {
                required,
            },
            sleep_usually: {
                required,
            },
            sleep_last_night: {
                required,
            },
            worn_biological_sensors: {
                required,
            },
            experiment_lab_environment: {
                required,
            },
            n_back_knowledge: {
                required,
            },
            prescription_drug: {
                required,
            },
            recreational_drug: {
                required,
            },
            ethnicity: {
                required,
            }
        }
    },

  methods: {

    getSubjectID() {
      let backend_url = this.$store.state.backend_url;
      let path = backend_url + "/get_subject_id";
      axios
        .get(path)
        .then((res) => {
          let sub_id = res.data;
          this.subject_id = sub_id;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    submit() {
        let backend_url = this.$store.state.backend_url;
        let path = backend_url + "/save_pre_experiment_result";
        let result = this.result;

        console.log('submit!');
        this.$v.$touch();

        if (this.$v.$invalid) {
            this.submitStatus = 'ERROR'
        } else {
            // Send the result data to the backend
            axios
            .post(path, result)
            .then((response) => {
                console.log(response);
            })
            .catch((error) => {
                console.error(error);
            });

            // Make sure the backend successfully initialize muse receiver
            // Then go to experiment
            this.loadNext();
        }
    },

        loadNext() {
            this.$router.replace(this.next);
        },
    },
};
</script>

<style lang="scss" scoped>
    .typo__p {
        color: #ff0000;
        text-align: center;
    }

    .input_text {
        box-sizing: border-box;
        text-align: left;
        font-size: medium;
        height: 1.5em;
        border-radius: 4px;
        border:2px solid #c8cccf;
        color: #6a6f77;
        display: block;
        outline: 0;
        padding: 0 0.5em;
        text-decoration: none;
        width: 30%;
    }

    .valid-feedback {
        font-size: medium;
    }

    .invalid-feedback {
        color: #ff0000;
        font-size: medium;
    }

    h3 {
        font-size: larger;
    }

    input[type="radio"]{
        margin: 0 10px 0 10px;
        vertical-align: middle;
        width: 30px;
        height: 1em;
    }

    input[type="number"]{
        text-align: left;
        font-size: medium;
        border: 2px solid #c8cccf;
        color: #000000;
        width: 30%;
    }

    input[type="checkbox"]{
        margin: 0 10px 0 10px;
        vertical-align: middle;
        width: 30px;
        height: 1em;
    }

    textarea {
        font-size: large;
    }

    label {
        font-size: large;
        font-weight: normal;
        margin: 2px;
        margin-right: 70px;
    }

    hr {
        border-top: 1px solid #8c8b8b; 
    }

    p {
        font-size: large;
        font-weight: normal;
    }

    li {
        font-size: large;
        font-weight: normal;
    }

    button {
        margin: 0 auto;
    }
</style>