<template>
    <div>
        <!-- <h1>General Introduction</h1> -->
        <div class="video_box">
            <video ref="videoPlayer" class="video-js">
            <source
                :src="srcurl"
                type="video/mp4"
            />
            </video>
        </div>
        <!-- <center><button @click="loadNext">Next</button></center> -->
    </div>
</template>

<script>

export default {
    name: "GeneralIntro",

    data() {
        return {
            next: {name: "wait_device_put_on"},
            player: null,
            srcurl: require("@/../public/static/" + this.$store.state.experiment_parameters.introductionVideoPath),
        };
    },

    mounted() {
        this.initVideo();
    },

    methods: {
        initVideo() {
            let options = {
                controls: false, // not show the control bar
                preload: "auto",
                //  comment the line below to pass the general intro video
                autoplay: true,
            };

            let vm = this;
            this.player = this.$video(this.$refs.videoPlayer, options, function () {
                this.on('ended', function() {
                    vm.loadNext();
                    console.log("General intro video ends");
                });
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
        // margin-top: 50px;
        font-size: xx-large;
    }

    button {
        width: 100px;
        height: 50px;
        font-size: x-large;
        margin-top: 10px;
    }

</style>