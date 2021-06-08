<template>
    <div>
        <h1>Please wait for the operator to help you take off the headband device</h1>
        <center><button v-if="show_button" @click="loadNext">Next</button></center>
    </div>
</template>

<script>
import { Howl } from "howler"; // used to play audio

export default {
    name: "WaitDeviceTakeOff",

    data() {
        return {
            next: {name: "post_exp_form_container"},
            time_button_show: 60,
            show_button: false,
        };
    },

    mounted() {
        setTimeout(() => {
            this.show_button = true;
        }, (this.time_button_show) * 1000);

        let audio_file = require("@/../public/static/wait_device_taking_off.mp3");
        this.audio = new Howl({src: audio_file});
        this.audio.play();
    },

    methods: {
        loadNext() {
            this.$router.replace(this.next);
        },
    },
};
</script>

<style lang="scss" scoped>
    h1 {
        color: #ffffff;
        margin-top: 200px;
        font-size: 250%;
    }

    button {
        width: 100px;
        height: 50px;
        font-size: x-large;
        margin-top: 10px;
    }

</style>