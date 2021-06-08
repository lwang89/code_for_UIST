<template>
  <div class="card">
    <h3 class="card-header text-center">Register Area</h3>
    <div class="card-body">
      <form @submit.prevent="submit">
        <div class="form-row">
          <div class="form-group col-md-6">
            <label>First Name</label>
            <input type="text" class="form-control" v-model.trim="$v.result.firstname.$model" :class="{'is-invalid': $v.result.firstname.$error, 'is-valid': !$v.result.firstname.$invalid}">
            <div class="valid-feedback">Your first name is valid!</div>
            <div class="invalid-feedback">
              <span v-if="!$v.result.firstname.required">First name is required.</span>
              <span v-if="!$v.result.firstname.minLength">First name must have at least {{$v.result.firstname.$params.minLength.min}} letters.</span>
              <span v-if="!$v.result.firstname.maxLength">First name must have at most {{$v.result.firstname.$params.maxLength.max}} letters.</span>
            </div>
          </div>
          <div class="form-group col-md-6">
            <label>Last Name</label>
            <input type="text" class="form-control" v-model.trim="$v.result.lastname.$model" :class="{'is-invalid': $v.result.lastname.$error, 'is-valid': !$v.result.lastname.$invalid}">
            <div class="valid-feedback">Your last name is valid!</div>
            <div class="invalid-feedback">
              <span v-if="!$v.result.lastname.required">Last name is required.</span>
              <span v-if="!$v.result.lastname.minLength">Last name must have at least {{$v.result.lastname.$params.minLength.min}} letters.</span>
              <span v-if="!$v.result.lastname.maxLength">First name must have at most {{$v.result.lastname.$params.maxLength.max}} letters.</span>
            </div>
          </div>
        </div>
        <div class="form-group">
          <label>Age</label>
          <input type="number" class="form-control" v-model.number="$v.result.age.$model" :class="{'is-invalid': $v.result.age.$error, 'is-valid': !$v.result.age.$invalid}">
          <div class="valid-feedback">Your age is valid!</div>
          <div class="invalid-feedback">
            <span v-if="!$v.result.age.required">Age is required.</span>
            <span v-if="!$v.result.age.between">Must between {{$v.result.age.$params.between.min}} and {{$v.result.age.$params.between.max}}.</span>
          </div>
        </div>

        <button class="button" type="submit" :disabled="submitStatus === 'PENDING'">Submit!</button>
        <p class="typo__p" v-if="submitStatus === 'OK'">Thanks for your submission!</p>
        <p class="typo__p" v-if="submitStatus === 'ERROR'">Please fill the form correctly.</p>
        <p class="typo__p" v-if="submitStatus === 'PENDING'">Sending...</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { required, minLength, maxLength, between } from 'vuelidate/lib/validators';

export default {
  name: "FormValidation",

  data() {
    return {
      next: {name: "experiment"},
      result: {
        firstname: "",
        lastname: "",
        age: "",
      },
      submitStatus: null,
    };
  },

  validations: {
    result:{
        firstname: {
        required,
        minLength: minLength(1),
        maxLength: maxLength(10)
      },
      lastname: {
        required,
        minLength: minLength(5),
        maxLength: maxLength(12)
      },
      age: {
        required,
        between: between(15, 40)
      }
    }
  },

  methods: {
    submit() {
      let backend_url = this.$store.state.backend_url;
      let path = backend_url + "/post_pre_experiment_results";
      let result = this.result;

      console.log('submit!');
      this.$v.$touch();
      if (this.$v.$invalid) {
        this.submitStatus = 'ERROR'
      } else {
        axios
        .post(path, result)
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.error(error);
        });
        // do your submit logic here
        this.submitStatus = 'PENDING'
        setTimeout(() => {
          this.submitStatus = 'OK'
        }, 500)
        this.loadNext();
      }
    },

    loadNext() {
      this.$router.replace(this.next);
    },
  }
}
</script>

<style scoped>
</style>