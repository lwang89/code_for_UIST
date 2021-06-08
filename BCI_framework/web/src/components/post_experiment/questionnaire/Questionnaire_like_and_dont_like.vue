<template>
    <div class="card">
        <h3 class="card-header text-center">Questionnaire</h3>
        <div class="card-body">
            <form @submit.prevent="submit">
                <ol>
                    <!-- text -->
                    <!-- Return: Things like-->
                    <li><label>Things you like</label></li>
                    <textarea type="text" placeholder="please input text" class="form-control input" v-model.trim="$v.result.like.$model" :class="{'is-invalid': $v.result.like.$error, 'is-valid': !$v.result.like.$invalid}"></textarea>
                    <div class="invalid-feedback">
                        <span v-if="!$v.result.like.required">Please input your answer.</span>
                    </div>

                    <!-- text -->
                    <!-- Return: Things don't like-->
                    <li><label>Things you don't like</label></li>
                    <textarea type="text" placeholder="please input text" class="form-control input" v-model.trim="$v.result.dont_like.$model" :class="{'is-invalid': $v.result.dont_like.$error, 'is-valid': !$v.result.dont_like.$invalid}"></textarea>
                    <div class="invalid-feedback">
                        <span v-if="!$v.result.dont_like.required">Please input your answer.</span>
                    </div>

                </ol>
                <p class="typo__p" v-if="submitStatus === 'ERROR'">Please fill the form correctly.</p>
            </form>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { required } from 'vuelidate/lib/validators';

export default {
    name: "Questionnaire_like_and_dont_like",

    data() {
        return {
            next: {name: "finish"},
            result: {
                name        : "questionnaire_like_and_dont_like",                // Text
                like        : "",                               // Text
                dont_like   : "",                               // Text
            },
            submitStatus: null,
        };
    },

    validations: {
        result:{
            like: {
                required,
            },
            dont_like: {
                required,
            },
        }
    },

    methods: {
        submit() {
            let backend_url = this.$store.state.backend_url;
            let path = backend_url + "/save_post_experiment_results";

            console.log('submit!');
            this.$v.$touch();

            if (this.$v.$invalid) {
                this.submitStatus = 'ERROR'
            } else {
                axios
                    .post(path, this.result)
                    .then((response) => {
                        console.log(response);
                        this.loadNext();
                    })
                    .catch((error) => {
                        console.error(error);
                    });
            }
        },

        loadNext() {
            this.$router.replace(this.next);
        },
    },
};
</script>

<style lang="scss" scoped>
    .input {
        box-sizing: border-box;
        text-align: left;
        font-size: large;
        
        border-radius: 4px;
        border: 2px solid #c8cccf;
        color: #000000;
        display: block;
        outline: 0;
        padding: 0 0.5em;
        text-decoration: none;
        width: 60%;
        height: 5em;
    }

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

    textarea {
        font-size: large;
    }

	h3 {
        font-size: larger;
    }

    label {
        // font-size:large;
        font-weight:normal;
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
    
