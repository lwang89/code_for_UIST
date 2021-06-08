<template>
    <div class="card">
        <h3 class="card-header text-center">Questionnaire</h3>
        <div class="card-body">
            <form @submit.prevent="submit">
                <ol>
                    <!-- Radio -->
                    <!-- Return: Uncomfortable -->
                    <div class="form-group">
                        <li><label id="uncomfortable">Did you feel uncomfortable with the headband during the task?</label></li>

                        <input type="radio" id="uncomfortable_yes" value="yes" v-model="$v.result.uncomfortable.$model" :class="{'is-invalid': $v.result.uncomfortable.$error, 'is-valid': !$v.result.uncomfortable.$invalid}">
                        <label for="uncomfortable_yes">Yes</label>
                        <br/>

                        <input type="radio" id="uncomfortable_no" value="no" v-model="$v.result.uncomfortable.$model" :class="{'is-invalid': $v.result.uncomfortable.$error, 'is-valid': !$v.result.uncomfortable.$invalid}">
                        <label for="uncomfortable_no">No</label>
                        <br/>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.uncomfortable.required">Please select your answer.</span>
                        </div>
                    </div>

                    <hr />

                    <!-- Radio -->
                    <!-- Return: Movement -->
                    <div class="form-group">
                        <li><label id="movement">Was there any movement of the headband during the experiment?</label></li>

                        <input type="radio" id="movement_yes" value="yes" v-model="$v.result.movement.$model" :class="{'is-invalid': $v.result.movement.$error, 'is-valid': !$v.result.movement.$invalid}">
                        <label for="movement_yes">Yes</label>
                        <br/>

                        <input type="radio" id="movement_no" value="no" v-model="$v.result.movement.$model" :class="{'is-invalid': $v.result.movement.$error, 'is-valid': !$v.result.movement.$invalid}">
                        <label for="movement_no">No</label>
                        <br/>

                        <input type="radio" id="movement_uncertain" value="uncertain" v-model="$v.result.movement.$model" :class="{'is-invalid': $v.result.movement.$error, 'is-valid': !$v.result.movement.$invalid}">
                        <label for="movement_uncertain">Uncertain</label>
                        <br/>

                        <div class="invalid-feedback">
                            <span v-if="!$v.result.movement.required">Please select your answer.</span>
                        </div>
                    </div>
                </ol>
                <p class="typo__p" v-if="submitStatus === 'ERROR'">Please fill the form correctly.</p>
            </form>
        </div>
    </div>
</template>

<script>
// import axios from "axios";
import { required } from 'vuelidate/lib/validators';

export default {
    name: "Questionnaire_uncomfortable_movement",

    data() {
        return {
            next: {name: "nasa_tlx"},
            result: {
                // name: "questionnaire_1",    // Text
                movement: "",               // Radio: yes/no/uncertain
                uncomfortable: "",               // Radio: yes/no
            },
            submitStatus: null,
        };
    },

    validations: {
        result:{
            movement: {
                required,
            },
            uncomfortable: {
                required,
            },
        }
    },

    methods: {
        submit() {
            console.log('submit!');
            this.$v.$touch();

            if (this.$v.$invalid) {
                this.submitStatus = 'ERROR'
            } else {
                this.$store.state.serial_feedback = this.result;
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

    .valid-feedback {
        font-size:medium;
    }

    .invalid-feedback {
        color: #ff0000;
        font-size:medium;
    }

    input[type="radio"]{
        margin: 0 10px 0 10px;
        vertical-align: middle;
        width: 30px;
        height: 1em;
    }

    h3 {
        font-size: larger;
    }
    
    label {
        // font-size: large;
        font-weight: normal;
        margin: 2px;
        margin-right: 70px;
    }

    p {
        font-size: large;
        font-weight: normal;
    }

    li {
        // font-size: large;
        font-weight: normal;
    }

    button {
        margin:0 auto;
    }
</style>