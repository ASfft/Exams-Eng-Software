Vue.component('true-false-component', {
    props: ['initial'],
    template: `
    <div>
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
            answer: this.initial || null
        }
    },
    watch: {
        answer(newValue) {
            this.$emit('input', newValue);
        }
    }
});

Vue.component('multiple-choice-component', {
    props: ['question', 'initial'],
    template: `
    <div>
      <div v-for="(choice, index) in question.choices" :key="index" class="input-group mb-3">
        <div class="input-group-text">
            <input type="radio" v-model="answer" :value="choice.text">{{ choice.text }}
        </div>
      </div>
    </div>
  `,
    data() {
        return {
            answer: this.initial || null
        }
    },
    watch: {
        answer(newValue) {
            this.$emit('input', newValue);
        }
    }
});

Vue.component('numeric-component', {
    props: ['initial'],
    template: `
    <div>
      <label for="data">Your answer</label>
      <input id="data" v-model="answer" class="form-control" type="number">
    </div>
  `,
    data() {
        return {
            answer: this.initial || null
        }
    },
    watch: {
        answer(newValue) {
            this.$emit('input', newValue);
        }
    }
});


Vue.component('exam-component', {
    props: ['initialQuestions', 'initialAnswers', 'timeLimit', 'examId'],
    data() {
        return {
            questions: JSON.parse(this.initialQuestions),
            currentQuestionIndex: 0,
            answers: JSON.parse(this.initialAnswers),
            remainingTime: this.timeLimit,
        };
    },
    created() {
        setInterval(async () => {
            if(this.remainingTime > 0) {
                this.remainingTime--;
            } else {
                await this.submitAnswer()
                window.location.href = `/exams/${this.examId}/details`;
            }
        }, 1000);
    },
    template: `
        <div class="container my-3">
            <div class="my-3">
                <h5>Time left: {{ formatTime(remainingTime) }}</h5>
            </div>
            <div v-if="questions.length > 0" class="card">
                <div class="card-body">
                    <h2 class="card-title">{{ questions[currentQuestionIndex].text }}</h2>
                    <p class="card-subtitle mb-2 text-muted">Value: {{ questions[currentQuestionIndex].value }}</p>
                    <multiple-choice-component 
                    v-if="questions[currentQuestionIndex].question_type.id === 1" 
                    :question="questions[currentQuestionIndex].data" 
                    :initial="answers[questions[currentQuestionIndex].id]" 
                    v-model="answers[questions[currentQuestionIndex].id]" 
                    class="my-3">
                    </multiple-choice-component>
                    <true-false-component 
                    v-if="questions[currentQuestionIndex].question_type.id === 2" 
                    :initial="answers[questions[currentQuestionIndex].id]" 
                    v-model="answers[questions[currentQuestionIndex].id]" 
                    class="my-3"></true-false-component>
                    <numeric-component 
                    v-if="questions[currentQuestionIndex].question_type.id === 3" 
                    :initial="answers[questions[currentQuestionIndex].id]" 
                    v-model="answers[questions[currentQuestionIndex].id]" 
                    class="my-3"></numeric-component>
                    <button @click="previousQuestion" v-if="currentQuestionIndex > 0" class="btn btn-primary">Previous question</button>
                    <button @click="nextQuestion" v-if="currentQuestionIndex < questions.length - 1" class="btn btn-primary">Next question</button>
                    <button @click="finishExam" v-if="currentQuestionIndex === questions.length - 1" class="btn btn-success">Finish Exam</button>
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
        async submitAnswer() {
            const currentQuestion = this.questions[this.currentQuestionIndex]
            const response = await fetch(`${this.examId}/submit_answer`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    questionId: currentQuestion.id,
                    answer: this.answers[currentQuestion.id]
                }),
            });
        },
        async nextQuestion() {
            await this.submitAnswer();
            this.currentQuestionIndex++;
        },
        async previousQuestion() {
            await this.submitAnswer();
            this.currentQuestionIndex--;
        },
        async finishExam() {
            await this.submitAnswer();
            window.location.href = `/exams/${this.examId}/details`;
        },
        formatTime(seconds) {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const remainingSeconds = seconds % 60;

            return [
                hours.toString().padStart(2, '0'),
                minutes.toString().padStart(2, '0'),
                remainingSeconds.toString().padStart(2, '0')
            ].join(':');
        }
    }
});
