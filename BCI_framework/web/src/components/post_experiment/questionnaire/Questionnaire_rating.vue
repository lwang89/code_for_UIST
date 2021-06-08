<template>
	<div class="card">
		<h3 class="card-header text-center">Questionnaire</h3>
		<div class="card-body">
			<form @submit.prevent="submit">
				<ol>
					<div class="form-group">
						<li><label>How much can you maintain concentration?</label></li>
						<star-rating v-model="$v.result.concentration.$model" :class="{'is-invalid': $v.result.concentration.$error, 'is-valid': !$v.result.concentration.$invalid}" :rating="initial_rating" :star-size="start_size" :show-rating="false"></star-rating>
						<div class="invalid-feedback">
							<span v-if="!$v.result.concentration.between">Please input your rating.</span>
						</div>
					</div>

					<div class="form-group">
						<li><label>How much is the study entertaining?</label></li>
						<star-rating v-model="$v.result.entertaining.$model" :class="{'is-invalid': $v.result.entertaining.$error, 'is-valid': !$v.result.entertaining.$invalid}" :rating="initial_rating" :star-size="start_size" :show-rating="false"></star-rating>
						<div class="invalid-feedback">
							<span v-if="!$v.result.entertaining.between">Please input your rating.</span>
						</div>
					</div>

					<div class="form-group">
						<li><label>Did you sit still through the experiment?</label></li>
						<star-rating v-model="$v.result.sit.$model" :class="{'is-invalid': $v.result.sit.$error, 'is-valid': !$v.result.sit.$invalid}" :rating="initial_rating" :star-size="start_size" :show-rating="false"></star-rating>
						<div class="invalid-feedback">
							<span v-if="!$v.result.sit.between">Please input your rating.</span>
						</div>
					</div>

				</ol>
				<p class="typo__p" v-if="submitStatus === 'ERROR'">Please fill the form correctly.</p>
			</form>
		</div>
	</div>
</template>

<script>
import axios from "axios";
import StarRating from 'vue-star-rating';
import { required, between } from 'vuelidate/lib/validators';

export default {
	name: "Questionnaire_rating",

	data() {
		return {
			next: {name: "questionnaire_like_and_dont_like"},
			result: {
				name          : "questionnaire_rating",                // Text
				concentration : 0,                                // Number 1-5
				entertaining  : 0,                                // Number 1-5
				sit           : 0,                                // Number 1-5
			},
			initial_rating    : 0,
			start_size        : 20,
			submitStatus      : null,
		};
	},

	components: {
		StarRating
	},

	validations: {
		result:{
			concentration: {
				required,
				between: between(1, 5)
			},
			entertaining: {
				required,
				between: between(1, 5)
			},
			sit: {
				required,
				between: between(1, 5)
			},
		}
	},

	methods: {
		submit() {
			let backend_url = this.$store.state.backend_url;
			let path = backend_url + "/save_post_experiment_results";

			console.log('submit!');
			this.$v.$touch();
			if (this.$v.$invalid) {
				this.submitStatus = 'ERROR'
			} else {
				axios
					.post(path, this.result)
					.then((response) => {
						console.log(response);
						this.loadNext(this.next);
					})
					.catch((error) => {
						console.error(error);
					});
				
			}
		},

		loadNext(next) {
				this.$router.replace(next);
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

	h3 {
        font-size: larger;
    }

	label {
		// font-size:large;
		font-weight:normal;
	}

	p {
		font-size: large;
		font-weight: normal;
	}

	li {
		// font-size: large;
		font-weight: normal;
	}

	button {
		margin: 0 auto;
	}
</style>
    
