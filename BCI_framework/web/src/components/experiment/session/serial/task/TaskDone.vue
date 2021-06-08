<template>
    <div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "TaskDone",

    data() {
        return {
            next: {name: "serial_form_container"},
            obj: null,
        };
    },

    mounted() {
        // console.log("task down");
        this.setupResultObj();
        this.postTaskEnd();
    },

    methods: {
        setupResultObj() {
            this.obj = {};

            /* Set up task result */
            this.obj.task_result = this.$store.state.currentTaskResults;

            /* Set up name of the result, which will be the name of the local csv file */
            let session_type = this.$store.state.currentSession.sessionType;
            let serial_id = this.$store.state.currentSerial.serialID;
            this.obj.name = "task_result_" + session_type + "_" + serial_id;

            /* Set up serial info*/
            this.obj.serial_info = this.$store.state.currentSerialInfo;
        },

        postTaskEnd() {
            let backend_url = this.$store.state.backend_url;
            let path = backend_url + "/end_task";

            let obj = this.obj;

            axios
                .post(path, obj)
                .then((response) => {
                    console.log(response);
                    this.loadNext();
                })
                .catch((error) => {
                    console.error(error);
                });
        },

        loadNext() {
            this.$router.replace(this.next);
        },
    }
};
</script>

<style lang="scss" scoped></style>
