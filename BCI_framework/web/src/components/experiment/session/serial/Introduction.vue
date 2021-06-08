Introduction.vue, the first page in a Serial that will be rendered. It display
intruction for current Serial. It will be directed to the Task in a few seconds,
like 2 seconds
<template>
    <div>
        <!-- <h1>This is Introduction page</h1> -->
        <h1>{{content}}</h1>
        <!-- <p>Please wait for {{showDuration}} seconds</p> -->
        <div>
            <img :src="image" style="width: 80%; height: 80%"/>
        </div>
        <!-- <button @click="skip">Next</button> -->
    </div>
</template>

<script>
import { Howl } from "howler"; // used to play audio

export default {
    name: "Introduction",

    data() {
        return {
            next: {name: "task_start"},
            duration: 5,
            interval: null,
            content: "Content here should be replaced",
            timeout: null,
            image: null,
        };
    },

    computed: {
        showDuration: function() {
            return this.duration;
        }
    },

    mounted() {
        this.setupIntroInfo();

        /* Start the count down of time left by every second */
        this.interval = setInterval(() => {
            this.duration = this.duration - 1;
        }, 1000);

        /* Stop the count down and start task */
        this.timeout = setTimeout(() => {
            if (this.interval) {
                clearInterval(this.interval);
                this.interval = null;
            }
            // console.log("intro time out to task start");
            this.loadNext();
        }, this.duration * 1000);
    },

    methods: {
        setupIntroInfo() {
            let currentSerial = this.$store.state.currentSerial;
            this.duration = currentSerial.introduction.duration;
            this.content = currentSerial.introduction.content;

            let img_url = currentSerial.introduction.img_url
            this.image = require('@/assets/' + img_url);

            let audio_url = currentSerial.introduction.audio_url;
            let audio_file = require("@/../public/static/" + audio_url);
            this.audio = new Howl({src: audio_file});
            this.audio.play();
        },

        skip() {
            if (this.interval) {
                clearInterval(this.interval);
                this.interval = null;
            }
            if (this.timeout) {
                clearTimeout(this.timeout);
                this.timeout = null;
            }
            
            // console.log("intro skip to task start");
            this.loadNext();
        },

        loadNext() {
            this.$router.replace(this.next);
        },
    },
};
</script>

<style lang="scss" scoped>
    button {
        width: 100px;
        height: 50px;
        font-size: medium;
        margin-top: 20px;
    }

    h1 {
        color: #ffffff;
        // margin-top: 100px;
        font-size: xx-large;
    }
</style>
