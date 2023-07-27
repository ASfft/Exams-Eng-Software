Vue.component('true-false-result-component', {
    props: ['initial'],
    template: `
    <div>
      <div class="form-check">
        <input class="form-check-input" type="radio" v-model="answer" id="true" value="True" disabled>
        <label class="form-check-label" for="true">
          True
        </label>
      </div>
      <div class="form-check">
        <input class="form-check-input" type="radio" v-model="answer" id="false" value="False" disabled>
        <label class="form-check-label" for="false">
          False
        </label>
      </div>
    </div>
  `,
    data() {
        return {
            answer: this.initial || null
        }
    }
});

Vue.component('multiple-choice-result-component', {
    props: ['question', 'initial'],
    template: `
    <div>
      <div v-for="(choice, index) in question.choices" :key="index" class="input-group mb-3">
        <div class="input-group-text">
            <input type="radio" v-model="answer" :value="choice.text" disabled>{{ choice.text }}
        </div>
      </div>
    </div>
  `,
    data() {
        return {
            answer: this.initial || null
        }
    }
});

Vue.component('numeric-result-component', {
    props: ['initial'],
    template: `
    <div>
      <label for="data">Your answer</label>
      <input id="data" v-model="answer" class="form-control" type="number" readonly>
    </div>
  `,
    data() {
        return {
            answer: this.initial || null
        }
    }
});


Vue.component('result-component', {
    props: ['initialQuestions', 'initialAnswers', 'examId'],
    data() {
        return {
            questions: JSON.parse(this.initialQuestions),
            currentQuestionIndex: 0,
            answers: JSON.parse(this.initialAnswers)
        };
    },
    computed: {
        currentQuestion() {
            return this.questions[this.currentQuestionIndex];
        },
        currentAnswer() {
            return this.answers[this.currentQuestion.id];
        },
        isCurrentAnswerCorrect() {
            return this.currentAnswer.toString() === this.currentQuestion.data.answer.toString();
        },
        correctAnswer() {
            return this.currentQuestion.data.answer;
        }
    },
    template: `
        <div class="container my-3">
            <div v-if="questions.length > 0" class="card">
                <div class="card-body">
                    <h2 class="card-title">{{ currentQuestion.text }}</h2>
                    <p class="card-subtitle mb-2 text-muted">Value: {{ currentQuestion.value }}</p>
                    <p v-if="isCurrentAnswerCorrect" class="text-success">Your answer is correct.</p>
                    <p v-else class="text-danger">Your answer is incorrect. The correct answer is: {{ correctAnswer }}</p>
                    <multiple-choice-result-component 
                    v-if="currentQuestion.question_type.id === 1" 
                    :question="currentQuestion.data" 
                    :initial="currentAnswer" 
                    v-model="currentAnswer" 
                    class="my-3">
                    </multiple-choice-result-component>
                    <true-false-result-component 
                    v-if="currentQuestion.question_type.id === 2" 
                    :initial="currentAnswer" 
                    v-model="currentAnswer" 
                    class="my-3"></true-false-result-component>
                    <numeric-result-component 
                    v-if="currentQuestion.question_type.id === 3" 
                    :initial="currentAnswer" 
                    v-model="currentAnswer" 
                    class="my-3"></numeric-result-component>
                    <button @click="previousQuestion" v-if="currentQuestionIndex > 0" class="btn btn-primary">Previous question</button>
                    <button @click="nextQuestion" v-if="currentQuestionIndex < questions.length - 1" class="btn btn-primary">Next question</button>
                    <button @click="goBack" v-if="currentQuestionIndex === questions.length - 1" class="btn btn-success">Go Back</button>
                </div>
            </div>
            <div v-else>
                <div class="alert alert-danger" role="alert">
                    No questions found.
                </div>
            </div>
        </div>
    `,
    methods: {
        nextQuestion() {
            if (this.currentQuestionIndex < this.questions.length - 1) {
                this.currentQuestionIndex++;
            }
        },
        previousQuestion() {
            if (this.currentQuestionIndex > 0) {
                this.currentQuestionIndex--;
            }
        },
        async goBack() {
            window.location.href = `/exams/${this.examId}/details`;
        },
    }
});