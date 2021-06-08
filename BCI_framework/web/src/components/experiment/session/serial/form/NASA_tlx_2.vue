<template>
    <div class="card">
        <h3 class="card-header text-center" id="title">NASA Workload Index</h3>
        <div class="card-body">
            <form @submit.prevent="submit">
                <ol>
                    <div class="form-group">
                        <li value="4"><label>Performance</label></li>
                        <p>How successful were you in accomplishing what you were asked to do?</p>
                        <vue-slider :style="slider_style" v-model="$v.result.performance.$model" :class="{'is-invalid': $v.result.performance.$error, 'is-valid': !$v.result.performance.$invalid}" :adsorb="true" :min="0" :max="100" :interval="5" :marks="marks_perfect_failure" :tooltip="tooltip_option">
                            <template v-slot:step="{ active }">
                                <div :class="['custom-step', { active }]"></div>
                            </template>
                        </vue-slider>
                        <br />
                        <div class="invalid-feedback">
                            <span v-if="!$v.result.performance.between">Please rate by sliding the bar.</span>
                        </div>
                        <br />
                    </div>

                    <hr />

                    <div class="form-group">
                        <li><label>Effort</label></li>
                        <p>How hard did you have to work to accomplish your level of performance?</p>
                        <vue-slider :style="slider_style" v-model="$v.result.effort.$model" :class="{'is-invalid': $v.result.effort.$error, 'is-valid': !$v.result.effort.$invalid}" :adsorb="true" :min="0" :max="100" :interval="5" :marks="marks_low_high" :tooltip="tooltip_option">
                            <template v-slot:step="{ active }">
                                <div :class="['custom-step', { active }]"></div>
                            </template>
                        </vue-slider>
                        <br />
                        <div class="invalid-feedback">
                            <span v-if="!$v.result.effort.between">Please rate by sliding the bar.</span>
                        </div>
                        <br />
                    </div>

                    <hr />

                    <div class="form-group">
                        <li><label>Frustration</label></li>
                        <p>How insecure, discouraged, irritated, stressed, and annoyed were you?</p>
                        <vue-slider :style="slider_style" v-model="$v.result.frustration.$model" :class="{'is-invalid': $v.result.frustration.$error, 'is-valid': !$v.result.frustration.$invalid}" :adsorb="true" :min="0" :max="100" :interval="5" :marks="marks_low_high" :tooltip="tooltip_option">
                            <template v-slot:step="{ active }">
                                <div :class="['custom-step', { active }]"></div>
                            </template>
                        </vue-slider>
                        <br />
                        <div class="invalid-feedback">
                            <span v-if="!$v.result.frustration.between">Please rate by sliding the bar.</span>
                        </div>
                        <br />
                    </div>
                </ol>
                <p class="typo__p" v-if="submitStatus === 'ERROR'">Please fill the form correctly.</p>
            </form>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'
import { required, between } from 'vuelidate/lib/validators';

export default {
    name: "NASA_tlx_2",

    data() {
        return {
            next: {name: "rest"},
            result: {
                name                : "nasa_tlx_",         // String
                performance         : -1,                   // Int
                effort              : -1,                   // Int
                frustration         : -1,                   // Int
            },
            slider_style    : "width:80%;",
            marks_low_high:
            {
                0: {label: "Very Low", labelStyle: {width: '70px', 'font-size':'large',}},
                5: "",
                10: "",
                15: "",
                20: "",
                25: {label: "|", labelStyle: {top: '-30px', left: "3px", 'font-size':'large',}},
                30: "",
                35: "",
                40: "",
                45: "",
                50: {label: "|", labelStyle: {top: '-30px', left: "3px", 'font-size':'large',}},
                55: "",
                60: "",
                65: "",
                70: "",
                75: {label: "|", labelStyle: {top: '-30px', left: "3px", 'font-size':'large',}},
                80: "",
                85: "",
                90: "",
                95: "",
                100: {label: "Very High", labelStyle: {width: '70px', left: '100%', 'font-size':'large',}},
            },
            marks_perfect_failure:
            {
                0: {label: "Perfect", labelStyle: {width: '70px', 'font-size':'large',}},
                5: "",
                10: "",
                15: "",
                20: "",
                25: {label: "|", labelStyle: {top: '-30px', left: "3px", 'font-size':'large',}},
                30: "",
                35: "",
                40: "",
                45: "",
                50: {label: "|", labelStyle: {top: '-30px', left: "3px", 'font-size':'large',}},
                55: "",
                60: "",
                65: "",
                70: "",
                75: {label: "|", labelStyle: {top: '-30px', left: "3px", 'font-size':'large',}},
                80: "",
                85: "",
                90: "",
                95: "",
                100: {label: "Failure", labelStyle: {width: '70px', left: '100%', 'font-size':'large',}},
            },
            tooltip_option: "none",
            submitStatus: null,
        };
    },

    components: {
        VueSlider
    },

    mounted() {
        this.setupName();
    },

    validations: {
        result:{
            performance: {
                required,
                between: between(0, 100)
            },
            effort: {
                required,
                between: between(0, 100)
            },
            frustration: {
                required,
                between: between(0, 100)
            }
        }
    },

    methods: {
        setupName() {
            let session_type = this.$store.state.currentSession.sessionType;
            let serial_id = this.$store.state.currentSerial.serialID;
            this.result.name = "nasa_workload_index_" + session_type + "_" + serial_id;
        },

        submit() {
            // Post the result for current session
            let backend_url = this.$store.state.backend_url;
            let path = backend_url + "/save_serial_feedback";

            console.log('submit!');
            this.$v.$touch();

            if (this.$v.$invalid) {
                this.submitStatus = 'ERROR'
            } else {
                let result = this.$store.state.nasa_tlx_result;
                Object.assign(result, this.result);
                axios
                    .post(path, result)
                    .then((response) => {
                        console.log(response);
                        // Go to Finish
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

    .custom-step {
        width: 150%;
        height: 150%;
        border-radius: 50%;
        box-shadow: 0 0 0 3px #ccc;
        background-color: #fff;
    }
    .custom-step.active {
        box-shadow: 0 0 0 3px #3498db;
        background-color: #3498db;
    }

    h3 {
        font-size: larger;
    }

    label {
        // font-size: large;
        font-weight: normal;
    }

    hr {
        border-top: 1px solid #8c8b8b; 
    }

    p {
        font-size: large;
        font-weight: normal;
    }

    li {
        // font-size: large;
        font-weight: normal;
    }
</style>
    
