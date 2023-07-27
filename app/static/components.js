// components.js
Vue.component('true-false-component', {
    props: ['initial'],
    template: `
    <div>
      <label for="data">Answer</label>
      <div class="form-check">
        <input class="form-check-input" type="radio" v-model="answer" id="true" value="True">
        <label class="form-check-label" for="true">
          True
        </label>
      </div>
      <div class="form-check">
        <input class="form-check-input" type="radio" v-model="answer" id="false" value="False">
        <label class="form-check-label" for="false">
          False
        </label>
      </div>
    </div>
  `,
    data() {
        return {
            answer: this.initial?.answer || ''
        }
    },
    watch: {
        answer(newValue) {
            this.$emit('update:data', {answer: newValue});
        }
    }
});

Vue.component('multiple-choice-component', {
    props: ['initial'],
    template: `
    <div>
      <label for="data">Choices</label>
      <div v-for="(choice, index) in choices" :key="index" class="input-group mb-3">
        <input type="text" v-model="choice.text" class="form-control" placeholder="Choice text">
        <div class="input-group-append">
          <div class="input-group-text">
            <input type="radio" v-model="answer" :value="choice.text">
          </div>
        </div>
      </div>
      <button type="button" class="btn btn-secondary" @click="addChoice">Add choice</button>
    </div>
  `,
    data() {
        return {
            choices: this.initial.choices || [{ text: '' }],
            answer: this.initial.answer || ''
        }
    },
    watch: {
        choices: {
            handler(newValue) {
                this.$emit('update:data', {choices: newValue, answer: this.answer});
            },
            deep: true
        },
        answer(newValue) {
            this.$emit('update:data', {choices: this.choices, answer: newValue});
        }
    },
    methods: {
        addChoice() {
            this.choices.push({ text: '' });
        }
    }
});

Vue.component('numeric-component', {
    props: ['initial'],
    template: `
    <div>
      <label for="data">Correct answer</label>
      <input id="data" v-model="answer" class="form-control" type="number">
    </div>
  `,
    data() {
        return {
            answer: this.initial.answer || null
        }
    },
    watch: {
        answer(newValue) {
            this.$emit('update:data', {answer: newValue});
        }
    }
});
