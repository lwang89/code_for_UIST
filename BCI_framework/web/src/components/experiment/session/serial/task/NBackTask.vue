NBackTask.vue. One implimentation of Task. In the future there could be more
types of Tasks. Each Task has "numberOfTrials" Trials. Like relationship between
Session and Serials, when "counterTrilas" reaches "numberOfTrials", Task is
done.
<template>
    <div>
        <!-- <label>N: {{bigN}}</label> -->
        <!-- <label>Type: {{printType}}</label> -->
        <h1>{{bigN}}-back task</h1>

        <Trial v-bind:current="current" v-bind:type="type" />
        <!-- <label id="printStack">Stack of numbers: {{printStack}}</label> -->
    </div>
</template>

<script>
import Trial from "./trial/Trial.vue";
import alert_mp3 from "@/../public/static/alert.mp3";
import { Howl } from "howler"; // used to play alert

export default {
    name: "NBackTask",

    components: {
        Trial,
    },

    data() {
        return {
            next: {name: "task_done"},
            isAlerted: true,

            sequence: [1, 2, 1],  // Array. a sequence to display. It will be randomly initialized by the initializeSequence method during mounted. Each element can be a natural number or so.
            current: null,        // Current element in the sequence to display. Passed to the sub-component Trial through v-bind
            TrialIndex: 0,        // Index of current element.
            terminated: true,     // Boolean. indicate if experiment is terminated or not.
            trialActivated: false,// Boolean. indicate if trial is activated.
            interval: null,       // JS setInterval variable. repeated function called every "intervalTime"
            timeout: null,        // Handler for trial to start and end
            waitTime: 3.5,        // wait time before displaying the first number after the alert starts. This should be greater than the duration of alert sound
            sound: null,          // The sound variable to be created by Howler.
            keyDownFlag: false,   // true or false. in each interval, change from 0 to 1 only once when user presses left arrow or right arrow. at the beginning of each interval, reset to false
            keyDownSequence: [0, 0, 0], // array of -1, 0, 1, record sequence of keydownSpace.

            // Default values will be replaced by parameters in created()
            numberOfTrials: -1,
            displayDuration: 1,   // time duration of diplaying a number, in milliseconds.
            trialDuration:1.5, // Interval between displaying two consecutive numbers and also keydown records, in milliseconds,
            bigN: 1,              // Positive integer. parameter N for n-back.
            type: 0,              // Int indicating type of n-back experiment. Will be passed to sub-component Trial through v-bind. 0 for the number, 1 for position and so on.
            printType: "Number",
            printStack: [],
        };
    },

    mounted() {
        let vm = this;
        this.initializeVars();
        this.addEventListenerKeyDown(vm);
        // this.addEventListenerPreventScrollPage();

        // this.test_generate_sequence();

        this.commence();
    },

    methods: {
        initializeVars() {
            let currentSerial = this.$store.state.currentSerial;
            console.log("Serial: "+currentSerial.serialID);
            this.displayDuration = currentSerial.trial.displayDuration;
            this.trialDuration = currentSerial.trial.trialDuration;
            this.bigN = currentSerial.trial.trialParameters.bigN;
            this.terminated = false;
            this.TrialIndex = 0;

            // Setup Nback Type
            let trialType = currentSerial.trial.trialParameters.trialType;
            if (trialType == "NBackNumberVisual") {
                this.type = 0;
                this.printType = "NBackNumberVisual"
            }

            // this.numberOfTrials = currentSerial.trial.numberOfTrials;
            // this.sequence = this.initializeSequence(1, 10, this.numberOfTrials, this.bigN);
            this.sequence = currentSerial.trial.sequence;
            this.numberOfTrials = this.sequence.length;

            this.initializeKeyDownSequence();

            // Initialize stack to print
            this.printStack = []
        },


        initializeKeyDownSequence() {
            let default_value = 0;
            this.keyDownSequence = Array(this.numberOfTrials).fill(default_value);
        },


        addEventListenerKeyDown(vm) {
            // event listener, for SPACE key pressed down
            // change keyDownFlag from false to true only once
            // set the current record in keyDownSequence to 1
            window.addEventListener("keydown", function(e) {
                let TrialIndex = vm.TrialIndex; // iniyially 0
                let keyDownFlag = vm.keyDownFlag; // iniyially 0
                let keyDownSequence = vm.keyDownSequence; // iniyially [0, 0, 0]
                let trialActivated = vm.trialActivated; // initially false

                let true_value = 1;
                let false_value = -1;
                if (e.keyCode == 37 && !keyDownFlag && trialActivated) {
                    vm.keyDownFlag = true;
                    keyDownSequence[TrialIndex] = true_value;
                    console.log(keyDownSequence);
                }
                else if (e.keyCode == 39 && !keyDownFlag && trialActivated) {
                    vm.keyDownFlag = true;
                    keyDownSequence[TrialIndex] = false_value;
                    console.log(keyDownSequence);
                }
            });
        },

        // commence the experiement when called
        commence() {
            // play the alert sound before experiment start if needed, then start trial
            if (this.isAlerted) {   // Initially true
                this.playAlert();
                this.timeout = setTimeout(() => {
                    this.beginTrial();
                }, this.waitTime * 1000);
            }
            else {
                this.beginTrial();
            }
        },

        // after alert played, trial start!
        // excecute fetchNumber() repeatedly
        beginTrial() {
            if (this.terminated) return 0;

            this.trialActivated = true;
            // The first try
            this.fetchNumber();
            // Then repeat
            this.interval = setInterval(() => {
                this.TrialIndex = this.TrialIndex + 1;
                this.fetchNumber();
            }, this.trialDuration * 1000);
        },

        // fetch a number from the sequence
        fetchNumber() {
            let TrialIndex = this.TrialIndex;
            let numberOfTrials = this.numberOfTrials;
            let sequence = this.sequence;

            if (TrialIndex > numberOfTrials - 1) {
                this.terminate();
                return 0;
            } else {
                // Initialize the current record
                this.keyDownFlag = false;
                // Load the element to display
                this.current = sequence[TrialIndex];

                // Add the element to the stack to show
                this.printStack.push(this.current);

                // The event listener will record the keydown

                // End remove the display after displayDuration
                setTimeout(() => {
                    this.current = null;
                }, this.displayDuration * 1000);
            }
        },

        // terminate the experiement
        terminate() {
            this.stopAlert();
            clearInterval(this.interval);
            clearTimeout(this.timeout);
            this.terminated = true;
            this.trialActivated = false;
            this.current = null;

            this.generateResult();

            this.loadNext();
        },

        // generate result for current serial, then add it to the result array for current session
        generateResult() {
            let bigN = this.bigN;
            let sequence = this.sequence;
            let keydownSpaceSequence = this.keyDownSequence;
            let gold_standard = this.getGoldStandard(sequence, this.bigN);
            let accuracy = this.getAccuracy(gold_standard, this.keyDownSequence);
            let defaultValueCount = this.getDefaultValueCount(this.keyDownSequence);

            let result = {
                bigN,
                sequence,
                keydownSpaceSequence,
                gold_standard,
                accuracy,
                defaultValueCount
            };
            console.log(result);

            this.$store.state.currentTaskResults = result;
        },

        getGoldStandard(sequence, bigN) {
            let len = sequence.length;
            if (len <= bigN) {
                console.log("N is too big! NULL returned");
                return null;
            }
            let gold_standard = Array(len).fill(-1);
            for (let i = bigN; i < len; i++) {
                if (sequence[i - bigN] == sequence[i]) {
                    gold_standard[i] = 1;
                }
            }
            return gold_standard;
        },

        getAccuracy(sequence_1, sequence_2) {
            let len1 = sequence_1.length;
            let len2 = sequence_2.length;
            if (len1 != len2) {
                console.log("Lengths are not matched! -1 returned");
                return -1;
            }
            let count = 0;
            for (let i = 0; i < len1; i++) {
                if (sequence_1[i] == sequence_2[i]) {
                    count++;
                }
            }
            let accuracy = count / len1;
            return accuracy;
        },

        getDefaultValueCount(sequence) {
            let default_value = 0;
            let count = 0;

            for(let i = 0; i < sequence.length; i++) {
                if (sequence[i] == default_value) {
                    count++;
                }
            }

            return count;
        },

        playAlert() {
            this.sound = new Howl({src: alert_mp3, volume:0.1});
            this.sound.play();
            this.sound.on("end", function() {
                console.log("Alert Played Successfully!");
            });
        },

        stopAlert() {
            this.sound.stop();
        },

        loadNext() {
            this.$router.replace(this.next);
        },
    },
};
</script>

<style lang="scss" scoped>
    label {
        color: #ffffff;
        margin-right: 70px;
        font-size: larger;
        font-weight: normal;
    }
    h1 {
        color: #ffffff;
        margin-top: 100px;
        font-size: xx-large;
    }

    #printStack {
        font-size: xx-large;
    }
    
</style>
