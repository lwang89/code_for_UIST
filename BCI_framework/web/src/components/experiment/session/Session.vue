Session.vue. There are two types of Session: "Train Session" and "Test Session"
Session will perform Serials "numberOfSerials" times. When "serialIndex" reaches
"numberOfSerials", Session is done. For implementation, see Rest.vue When
"sessionIndex" reaches "numberOfSessions", all sessions are done. See
SessionDone.vue for deails
<template>
    <div>
        <!-- <p>Session</p> -->
        <!-- <p>SessionIndex:{{ sessionIndex }}</p> -->
        <router-view></router-view>
    </div>
</template>

<script>

export default {
    name: "Session",

    data() {
        return {
            next: {name: "session_start"}
        };
    },

    // computed: {
    //   sessionIndex: function() {
    //     return this.$store.state.sessionIndex;
    //   }
    // },

    mounted() {
        this.loadNext();
    },

    methods: {
        loadNext() {
            this.$router.replace(this.next);
        },
    },
};
</script>

<style lang="scss" scoped></style>
