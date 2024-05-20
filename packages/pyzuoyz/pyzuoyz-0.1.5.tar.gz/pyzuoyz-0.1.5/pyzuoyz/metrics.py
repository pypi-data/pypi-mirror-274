from nltk.translate.bleu_score import sentence_bleu
import jieba
from rouge import Rouge

import warnings
warnings.filterwarnings("ignore")

# BLEU
def bleu_score(true_answer : str, generate_answer : str) -> float:
    # true_anser : 标准答案，str 类型
    # generate_answer : 模型生成答案，str 类型
    true_answers = list(jieba.cut(true_answer))
    generate_answers = list(jieba.cut(generate_answer))
    bleu_score = sentence_bleu(true_answers, generate_answers)
    return bleu_score

def rouge_score(true_answer : str, generate_answer : str) -> float:
    # true_anser : 标准答案，str 类型
    # generate_answer : 模型生成答案，str 类型
    rouge = Rouge()
    rouge_score = rouge.get_scores(generate_answer, true_answer)
    return rouge_score
