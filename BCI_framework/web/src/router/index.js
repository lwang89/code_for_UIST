import Vue from "vue";
import VueRouter from "vue-router";

import Start  from  "@/components/Start.vue";

import PreExperiment          from  "@/components/pre_experiment/PreExperiment.vue";
import FormContainer          from  "@/components/pre_experiment/FormContainer.vue";
import SubjectInformation     from  "@/components/pre_experiment/SubjectInformation.vue";
import GeneralIntro           from  "@/components/pre_experiment/GeneralIntro.vue";
import WaitDevicePutOn           from  "@/components/pre_experiment/WaitDevicePutOn.vue";
import RestBeforeExperiment   from  "@/components/pre_experiment/RestBeforeExperiment.vue";

import Experiment     from  "@/components/experiment/Experiment.vue";
import SessionStart   from  "@/components/experiment/session/SessionStart.vue";
import SessionDone    from  "@/components/experiment/session/SessionDone.vue";

import Serial         from  "@/components/experiment/session/serial/Serial.vue";
import Introduction   from  "@/components/experiment/session/serial/Introduction.vue";
import TaskStart      from  "@/components/experiment/session/serial/task/TaskStart.vue";
import Task           from  "@/components/experiment/session/serial/task/Task.vue";
import TaskDone       from  "@/components/experiment/session/serial/task/TaskDone.vue";
import SerialFormContainer  from  "@/components/experiment/session/serial/form/SerialFormContainer.vue";
import Questionnaire_uncomfortable_movement  from  "@/components/experiment/session/serial/form/Questionnaire_uncomfortable_movement.vue";
// import NASA_tlx_1    from  "@/components/experiment/session/serial/form/NASA_tlx_1.vue";
// import NASA_tlx_2    from  "@/components/experiment/session/serial/form/NASA_tlx_2.vue";
import NASA_tlx    from  "@/components/experiment/session/serial/form/NASA_tlx.vue";
import Rest           from  "@/components/experiment/session/serial/Rest.vue";

import PostExperiment   from  "@/components/post_experiment/PostExperiment.vue";
import WaitDeviceTakeOff           from  "@/components/post_experiment/WaitDeviceTakeOff.vue";
import PostExpFormContainer   from  "@/components/post_experiment/PostExpFormContainer.vue";

import Questionnaire_rating  from  "@/components/post_experiment/questionnaire/Questionnaire_rating.vue";
import Questionnaire_like_and_dont_like  from  "@/components/post_experiment/questionnaire/Questionnaire_like_and_dont_like.vue";

import Finish  from  "@/components/Finish.vue";

Vue.use(VueRouter);

// const originalReplace = VueRouter.prototype.replace;
// VueRouter.prototype.replace = function repalce(location, onResolve, onReject) {
//   if (onResolve || onReject) return originalReplace.call(this, location, onResolve, onReject)
//   return originalReplace.call(this, location).catch(err => err)
// };

const routes = [

  { path: "/start",  name: "start", component: Start },
  { path: "/pre_experiment",
    name: "pre_experiment",
    component: PreExperiment,
    children: [
      { path: "form_container",
        name: "form_container",
        component: FormContainer,
        children: [
          { path: "subject_information",  name: "subject_information", component: SubjectInformation }
        ]
      },
      { path: "wait_device_put_on",  name: "wait_device_put_on", component: WaitDevicePutOn },
      { path: "general_intro",  name: "general_intro", component: GeneralIntro },
      { path: "rest_before_experiment",  name: "rest_before_experiment", component: RestBeforeExperiment }
    ]
  },
  { path: "/experiment",
    name: "experiment",
    component: Experiment,
    children: [
      { path: "session_start",  name: "session_start", component: SessionStart },
      { path: "serial",
        name: "serial",
        component: Serial,
        children: [
          { path: "introduction", name: "introduction", component: Introduction },
          { path: "task_start", name: "task_start", component: TaskStart },
          { path: "task", name: "task", component: Task },
          { path: "task_done", name: "task_done", component: TaskDone },
          { path: "serial_form_container",
            name: "serial_form_container",
            component: SerialFormContainer,
            children: [
              { path: "questionnaire_uncomfortable_movement", name: "questionnaire_uncomfortable_movement", component: Questionnaire_uncomfortable_movement },
              { path: "nasa_tlx", name: "nasa_tlx", component: NASA_tlx },
            ]
          },
          { path: "rest", name: "rest", component: Rest },
        ]
      },
      { path: "session_done",  name: "session_done", component: SessionDone }
    ]

  },
  { path: "/post_experiment",
    name: "post_experiment",
    component: PostExperiment,
    children: [
      { path: "wait_device_take_off",  name: "wait_device_take_off", component: WaitDeviceTakeOff },
      { path: "post_exp_form_container",
        name: "post_exp_form_container",
        component: PostExpFormContainer,
        children: [
          { path: "questionnaire_rating", name: "questionnaire_rating", component: Questionnaire_rating },
          { path: "questionnaire_like_and_dont_like", name: "questionnaire_like_and_dont_like", component: Questionnaire_like_and_dont_like },
        ]
      },
    ]
  },
  { path: "/finish",  name: "finish", component: Finish},
];

const router = new VueRouter({
  routes,
});

export default router;
