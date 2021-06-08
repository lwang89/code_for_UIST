<template>
    <div>
        <h1>Please wait for the operator to help you put on the headband device</h1>
        <center><button v-if="show_button" @click="loadNext">Next</button></center>
    </div>
</template>

<script>
import { Howl } from "howler"; // used to play audio
import axios from "axios";

export default {
    name: "WaitDevicePutOn",

    data() {
        return {
            next: {name: "rest_before_experiment"},
            time_button_show: 60,
            show_button: false,
        };
    },

    mounted() {
        let audio_file = require("@/../public/static/wait_device_putting_on.mp3");
        this.audio = new Howl({src: audio_file});
        this.audio.play();

        this.postDeviceReady();
    },

    methods: {
        postDeviceReady() {
            let backend_url = this.$store.state.backend_url;
            let path = backend_url + "/post_device_ready";
            let postInfo = 'Response anything when device is ready';
            axios
                .post(path, postInfo)
                .then((response) => {
                    console.log(response);
                    this.show_button = true;
                })
                .catch((error) => {
                    console.error(error);
                });
            },

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