<template>
  <div class="UsagePart">
    <!-- input part -->
    <div class="input">
      <!-- header -->
      <h1>论文原文</h1>
      <!-- input box -->
      <el-input
          :rows="18"
          resize="none"
          type="textarea"
          class="reportInput"
          v-model="reportInput"
          placeholder="请输入报告原文"/>
      <!-- buttons -->
      <div class="buttons">
        <!-- upload button -->
        <el-upload
            ref="upload"
            class="uploadButton"
            action="http://localhost:8000/Uploading"
            :limit="1"
            :on-exceed="handleExceed"
            :on-success="handleSuccess"
            :auto-upload="false">
          <i class="ri-attachment-2"></i>
        </el-upload>
        <!-- commit button -->
        <el-button
            round
            plain
            type="primary"
            class="commitButton"
            @click="handleCommit">
          提交
        </el-button>
      </div>
    </div>
    <!-- output part -->
    <div class="output">
      <!-- score part -->
      <div class="scores">
        <!-- total score -->
        <div class="finalScore">
          <!-- title -->
          <div class="finalScoreTitle">
            <p class="finalScoreTitleContent">综合得分</p>
          </div>
          <!-- value -->
          <div class="finalScoreValue">{{ finalScoreValue }}</div>
        </div>
        <!-- radar chart -->
        <div ref="radarChart" class="scoreEChart"></div>
      </div>
      <!-- comment part -->
      <el-scrollbar class="comments">
        <p class="comment">评语：</p>
        <p class="commentContent" v-html="commentContent"></p>
      </el-scrollbar>
      <!-- advice part -->
      <el-scrollbar class="advices">
        <p class="advice">修改意见：<br></p>
        <p class="adviceContent" v-html="adviceContent"></p>
      </el-scrollbar>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, watch} from 'vue'
import * as echarts from 'echarts'
import axios from 'axios';
import {ElLoading, genFileId} from 'element-plus'

// backend url
const backend_url = 'http://localhost:8000/Committing'

// input
const reportInput = ref('')

// outputs
const finalScoreValue = ref('')
const commentContent = ref('')
const adviceContent = ref('')

// radar chart
const radarChart = ref(null)
let radarChartInstance = null
radarChart.value = undefined;
onMounted(() => {
  radarChartInstance = echarts.init(radarChart.value)
  const option = {
    title: {
      text: ''
    },
    tooltip: {
      position: function (point, params, dom, rect, size) {
        // point: [x coordinate of mouse, y coordinate of mouse]
        const x = point[0];
        const y = point[1];
        // ensure the tooltip is within the visible area of the window
        const tooltipWidth = size.contentSize[0];
        const tooltipHeight = size.contentSize[1];
        // move to the left and down, incase it may be out of the window
        return [
          Math.max(x - tooltipWidth - 10, 0), // margin left 10px
          Math.min(y + 10, window.innerHeight - tooltipHeight) // margin down 10px
        ];
      }
    },
    radar: {
      indicator: [
        {name: '结构完整性', max: 10},
        {name: '逻辑清晰度', max: 10},
        {name: '语言连贯性', max: 10},
        {name: '内容创新性', max: 10},
        {name: '引用规范性', max: 10},
        {name: '知识掌握度', max: 10},
      ]
    },
    series: [{
      name: '各项得分',
      type: 'radar',
      data: [{
        value: [0, 0, 0, 0, 0, 0],
        name: '各项得分'
      }]
    }]
  }
  radarChartInstance.setOption(option)
})

// typing
const typingSpeed = 1;
let typingTimeouts = [];

// handle uploading
const upload = ref()
const uploadCondition = ref(false)
const handleExceed = (files) => {
  upload.value.clearFiles()
  const file = files[0]
  file.uid = genFileId()
  upload.value.handleStart(file)
  // console.log('File uploaded:\n', upload)
}
const handleSuccess = () => {
  uploadCondition.value = true
}

// typing animation
function typeText(targetRef, text, onComplete = () => {
}) {
  // reset typed content
  let currentIndex = 0;
  targetRef.value = '';
  typingTimeouts.forEach(timeout => clearTimeout(timeout));

  function type() {
    if (currentIndex < text.length) {
      targetRef.value += text.charAt(currentIndex);
      currentIndex++;
      const timeoutId = setTimeout(type, typingSpeed);
      typingTimeouts.push(timeoutId);
    } else {
      // typing completed and callback
      onComplete();
    }
  }

  type();
}

// handle commit
async function handleCommit() {
  if (reportInput.value === '' && upload.value === null) {
    alert('不能提交空白内容，请输入报告原文并再次尝试！')
  } else {
    // start to show loading
    const loadingInstance = ElLoading.service({fullscreen: true, lock: true, text: '提交中，请稍后...'})
    // reset all values
    finalScoreValue.value = ''
    commentContent.value = ''
    adviceContent.value = ''
    typingTimeouts.forEach(timeout => clearTimeout(timeout));
    radarChartInstance.setOption({
      series: [{
        data: [{
          value: [0, 0, 0, 0, 0, 0],
          name: '各项得分'
        }]
      }]
    })
    const radar = [];
    // send request
    try {
      // fake API
      const comment_examples = [
        "文章结构清晰，逻辑严谨，但部分内容需要进一步扩展。",
        "引用部分格式规范，但创新性不足，建议补充相关研究。",
        "内容全面，语言流畅，但缺少数据支持，建议增加具体案例。",
        "逻辑思路有些混乱，建议调整章节顺序，增强文章连贯性。",
        "写作思路清晰，参考文献引用合理，但部分论点有待进一步论证。",
        "语言表述精炼，内容详实，但需要补充相关背景信息。",
        "整体写作较好，创新性突出，但引用格式稍有不规范，建议修改。",
        "文章具有较好的连贯性，但细节部分略显单薄，建议充实。",
        "参考文献较全面，建议在结论部分增加对未来研究的展望。",
        "结构合理，分析深入，但部分论点阐述不够详细，建议补充。"
      ];
      const advice_examples = [
        "建议优化论文的结构，使得各部分衔接更加流畅。",
        "引用文献格式需统一，建议按照期刊要求进行修改。",
        "文章创新性较强，但部分论据较为薄弱，建议补充更有力的证据。",
        "在分析过程中，建议增加数据支持，增强文章的说服力。",
        "内容较为全面，但缺少部分关键领域的探讨，建议补充。",
        "建议重新审视结论部分，增强论证的深度和广度。",
        "部分论点表述模糊，建议进一步明确和具体化。",
        "建议补充更多的图表，以增加文章的可读性。",
        "建议参考更多的最新研究，以增强论文的前沿性。",
        "建议对不同观点进行更深入的对比分析，增加论述的深度。"
      ];
      const response_fake = {
        data: {
          success: true,
          score: (Math.random() * 10).toFixed(1),
          radar: [
            Math.floor(Math.random() * 10),
            Math.floor(Math.random() * 10),
            Math.floor(Math.random() * 10),
            Math.floor(Math.random() * 10),
            Math.floor(Math.random() * 10),
            Math.floor(Math.random() * 10)],
          comments: comment_examples[Math.floor(Math.random() * comment_examples.length)],
          advices: advice_examples[Math.floor(Math.random() * advice_examples.length)]
        }
      }
      // send uploading request
      // console.log('uploading process start')
      upload.value.submit()
      while (!uploadCondition) {

      }
      upload.value.clearFiles()
      uploadCondition.value = false
      // console.log('uploading process finish')
      // send committing request
      // console.log('committing process start')
      // console.log(reportInput.value)
      const response = await axios.post(backend_url, {
        text: reportInput.value
      });
      // console.log('committing process finish')
      // check response
      if (response.status === 200 && response.statusText === 'OK' && response.data.return !== "None") {
        // parse response into 8 parts (1 final score & 6 comments & 1 advice)
        const results = response.data.return.split('\n')
        // console.log('results:\n', results)
        results.forEach(line => {
          if (line.startsWith('最终打分：')) {
            // get final score
            const finalScoreMatch = line.match(/最终打分：(\d+(\.\d+)?) \(范围0-10分\)/);
            finalScoreValue.value = finalScoreMatch ? parseFloat(finalScoreMatch[1]).toFixed(1) : null;
          } else if (line.match(/\d+\. /)) {
            const details = line.split('得分：')[1];
            const [scorePart, reasonPart] = details.split('原因如下：');
            const score = scorePart.match(/(\d+)/)[0].trim();
            const reason = reasonPart.trim();
            // get comment content
            commentContent.value += (line + "<br>");
            // get radar
            radar.push(parseFloat(score));
          } else if (line.startsWith('修改意见：')) {
            // get advice content
            adviceContent.value = line.split('修改意见：')[1]
          }
        });
        // console.log('finalScoreValue: ', finalScoreValue.value)
        // console.log('radar: ', radar)
        // console.log('commentContent: ', commentContent.value)
        // console.log('adviceContent: ', adviceContent.value)
        // update radar chart
        radarChartInstance.setOption({
          series: [{
            data: [{
              value: radar,
              name: '各项得分'
            }]
          }]
        })
        // type content
        const commentText = commentContent.value;
        const adviceText = adviceContent.value;
        commentContent.value = ''
        adviceContent.value = ''
        typeText(commentContent, commentText, () => {
          // start to type advice content after comment content is fully typed
          typeText(adviceContent, adviceText);
        });
      } else {
        alert('提交失败，请稍后再试');
      }
    } catch (error) {
      // console.error('Error during commit:', error);
      alert('An error occurred during commit.');
    } finally {
      // stop loading
      loadingInstance.close();
    }
  }
}
</script>

<style>
/* usage part */
.UsagePart {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
}

.UsagePart .input, .UsagePart .output {
  margin: 0 auto;
  background-color: #f5f5f5;
  flex: 1;
  border: black 1px solid;
}

.UsagePart .input {
  text-align: center;
  left: 0;
}

.UsagePart .output {
  right: 0;
  display: flex;
  flex-direction: column;
}

/* input */
.UsagePart .input .reportInput {
  display: block;
  margin: 0 auto;
  width: 80%;
  height: 70%;
}

.UsagePart .input .reportInput .el-input__wrapper input {
  margin-top: 0;
}

.UsagePart .input .buttons {
  display: flex;
  margin: 0 auto;
  width: 80%;
  flex-direction: row;
}

.UsagePart .input .buttons .uploadButton {
  display: block;
  margin: 0 auto;
  flex: 5;
}

.UsagePart .input .buttons .uploadButton .ri-attachment-2 {
  font-size: 1.5em;
}

.UsagePart .input .buttons .commitButton {
  display: block;
  margin: 0 auto;
  flex: 1;
}

/* output (3 parts: score, comments, advice) */
.UsagePart .output .scores {
  text-align: left;
  display: flex;
  flex: 8;
  flex-direction: row;
}

.UsagePart .output .comments, .UsagePart .output .advices {
  text-align: left;
  border-top: black 1px solid;
  padding: 5px;
}

.UsagePart .output .comments {
  flex: 5;
}

.UsagePart .output .advices {
  flex: 3;
}

/* output-scores (2 parts: final score, scoreEChart) */
.UsagePart .output .scores .finalScore {
  flex: 2;
  display: flex;
  flex-direction: column;
}

.UsagePart .output .scores .finalScore .finalScoreTitle {
  flex: 2;
  position: relative;
  text-align: center;
}

.UsagePart .output .scores .finalScore .finalScoreTitle .finalScoreTitleContent {
  position: absolute;
  width: 100%;
  bottom: 0;
  margin: 0;
}

.UsagePart .output .scores .finalScore .finalScoreValue {
  flex: 3;
  color: limegreen;
  font-size: 3em;
  margin: 0 auto;
}

.UsagePart .output .scores .scoreEChart {
  flex: 3;
  height: 100%; /* must set a height in order to show the chart */
}

/* comment & advice (title) */
.UsagePart .output .comments .comment, .UsagePart .output .advices .advice {
  color: blue;
  margin: 0 auto 5px;
  padding: 0;
}

/* comment & advice (content) */
.UsagePart .output .comments .commentContent, .UsagePart .output .advices .adviceContent {
  margin: 0;
  padding: 0;
}
</style>
