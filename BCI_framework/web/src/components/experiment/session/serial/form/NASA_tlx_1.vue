<template>
    <div class="card">
        <h3 class="card-header text-center" id="title">NASA Workload Index</h3>
        <div class="card-body">
            <form @submit.prevent="submit">
                <ol>
                    <div class="form-group">
                        <li><label>Mental Demand</label></li>
                        <p>How mentally demanding was the task?</p>
                        <vue-slider :style="slider_style" v-model="$v.result.mental.$model" :class="{'is-invalid': $v.result.mental.$error, 'is-valid': !$v.result.mental.$invalid}" :adsorb="true" :min="0" :max="100" :interval="5" :marks="marks_low_high" :tooltip="tooltip_option">
                            <template v-slot:step="{ active }">
                                <div :class="['custom-step', { active }]"></div>
                            </template>
                        </vue-slider>
                        <br />
                        <div class="invalid-feedback">
                            <span v-if="!$v.result.mental.between">Please rate by sliding the bar.</span>
                        </div>
                        <br />
                    </div>

                    <hr />

                    <div class="form-group">
                        <li><label>Physical Demand</label></li>
                        <p>How physically demanding was the task?</p>
                        <vue-slider :style="slider_style" v-model="$v.result.physical.$model" :class="{'is-invalid': $v.result.physical.$error, 'is-valid': !$v.result.physical.$invalid}" :adsorb="true" :min="0" :max="100" :interval="5" :marks="marks_low_high" :tooltip="tooltip_option">
                            <template v-slot:step="{ active }">
                                <div :class="['custom-step', { active }]"></div>
                            </template>
                        </vue-slider>
                        <br />
                        <div class="invalid-feedback">
                            <span v-if="!$v.result.physical.between">Please rate by sliding the bar.</span>
                        </div>
                        <br />
                    </div>

                    <hr />

                    <div class="form-group">
                        <li><label>Temporal Demand</label></li>
                        <p>How hurried or rushed was the pace of the task?</p>
                        <vue-slider :style="slider_style" v-model="$v.result.temporal.$model" :class="{'is-invalid': $v.result.temporal.$error, 'is-valid': !$v.result.temporal.$invalid}" :adsorb="true" :min="0" :max="100" :interval="5" :marks="marks_low_high" :tooltip="tooltip_option">
                            <template v-slot:step="{ active }">
                                <div :class="['custom-step', { active }]"></div>
                            </template>
                        </vue-slider>
                        <br />
                        <div class="invalid-feedback">
                            <span v-if="!$v.result.temporal.between">Please rate by sliding the bar.</span>
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
// import axios from "axios";
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'
import { required, between } from 'vuelidate/lib/validators';

export default {
    name: "NASA_tlx_1",

    data() {
        return {
            next: {name: "nasa_tlx_2"},
            result: {
                // name                : "nasa_workload_index_",       // String
                mental              : -1,                           // Int
                physical            : -1,                           // Int
                temporal            : -1,                           // Int
            },
            slider_style    : "width:80%;",
            marks_low_high:
            {
                0: {label: "Very Low", labelStyle: {width: '70px', 'font-size':'large'}},
                5: "",
                10: "",
                15: "",
                20: "",
                25: {label: "|", labelStyle: {top: '-30px', left: "3px", 'font-size':'large'}},
                30: "",
                35: "",
                40: "",
                45: "",
                50: {label: "|", labelStyle: {top: '-30px', left: "3px", 'font-size':'large'}},
                55: "",
                60: "",
                65: "",
                70: "",
                75: {label: "|", labelStyle: {top: '-30px', left: "3px", 'font-size':'large'}},
                80: "",
                85: "",
                90: "",
                95: "",
                100: {label: "Very High", labelStyle: {width: '70px', left: '100%', 'font-size':'large'}},
            },
            tooltip_option: "none",
            submitStatus: null,
        };
    },

    components: {
        VueSlider
    },

    mounted() {
        // this.setupName();
        // console.log("nasa tlx 1");
    },

    validations: {
        result:{
            mental: {
                required,
                between: between(0, 100)
            },
            physical: {
                required,
                between: between(0, 100)
            },
            temporal: {
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
            console.log('submit!');
            this.$v.$touch();

            if (this.$v.$invalid) {
                this.submitStatus = 'ERROR'
            } else {
                let result = this.$store.state.nasa_tlx_result;
                Object.assign(result, this.result);
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
        // font-size: larger;
        font-weight: normal;
    }
</style>
    
