try:
    import reportlab
except ImportError:
    print "Failed import reportlab module."
    print "Download from http://www.reportlab.com/opensource/, and install:"
    print "    python setup.py install"
    exit()

import string
from optparse import OptionParser
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def drawPage(canvas, pageWidth, pageHeight,
             left, top, bottom,
             fontSize, fontLineRatio,
             questions):
    realHeight = pageHeight - top - bottom

    lineHeight = int(fontSize / fontLineRatio)
    maxLineCount = int(realHeight / lineHeight)

    allQuestions = questions

    while(True):
        questions = allQuestions
        if(len(questions) > (maxLineCount * 2)):
            questions = questions[0:maxLineCount * 2]

        rowCount_left = int(len(questions) / 2)
        if(rowCount_left * 2 != len(questions)):
            rowCount_left += 1

        canvas.setLineWidth(.1)
        canvas.setFont('Helvetica', fontSize)

        drawPosition_vertical = pageHeight - top
        drawPosition_horizontal = left
        for theQuestion in questions[0:rowCount_left]:
            canvas.drawString(drawPosition_horizontal, drawPosition_vertical, theQuestion)
            drawPosition_vertical -= lineHeight

        drawPosition_vertical = pageHeight - top
        drawPosition_horizontal = int(pageWidth / 2) + 30
        for theQuestion in questions[rowCount_left:]:
            canvas.drawString(drawPosition_horizontal, drawPosition_vertical, theQuestion)
            drawPosition_vertical -= lineHeight

        allQuestions = allQuestions[len(questions):]
        if(len(allQuestions) > 0):
            canvas.showPage()
        else:
            break


if __name__ == '__main__':
    optParser = OptionParser()

    optParser.add_option("-o", "--output-file", action = "store",
                         dest = "OutputFile",
                         default = "exam.pdf",
                         help = "Specify output file name (Default is exam.pdf)")
    optParser.add_option("-m", "--max-number", action = "store",
                         type = "int",
                         dest = "MaxNumber",
                         default = 10,
                         help = "Max number (Default is 10)")
    optParser.add_option("-c", "--questions-count", action = "store",
                         type = "int",
                         dest = "QuestionsCount",
                         default = 20,
                         help = "Questions count (Default is 20)")
    optParser.add_option("-r", "--repeat-times", action = "store",
                         type = "int",
                         dest = "RepeatTimes",
                         default = 1,
                         help = "Repeat times (Default is 1)")
    optParser.add_option("-f", "--font-size", action = "store",
                         type = "int",
                         dest = "FontSize",
                         default = 12,
                         help = "Font Size (Default is 12)")

    options,args = optParser.parse_args()

    outputFile = options.OutputFile
    maxNumber = options.MaxNumber
    questionsCount = options.QuestionsCount
    repeatTimes = options.RepeatTimes
    fontSize = options.FontSize

    canvas = canvas.Canvas(outputFile, pagesize=letter)
    pageWidth, pageHeight = letter

    for repeatIndex in range(repeatTimes):
        questionsList = []
        questionsWithIndexList = []

        maxIndexWidth = len(str(questionsCount))
        for i in range(1, questionsCount + 1):
            for repeat in range(10): # repeat 10 times to avoid duplicate
                leftValue = random.randint(1, maxNumber - 1)
                rightValue = random.randint(1, maxNumber - leftValue)
                operator = '+'

                isPlus = random.choice([True, False])
                if((not isPlus) and (leftValue < rightValue)):
                    leftValue, rightValue = rightValue, leftValue
                    operator = '-'

                indexStr = '{0})'.format(i).rjust(maxIndexWidth + 1)
                question = '{0} {1} {2} = '.format(leftValue, operator, rightValue)

                questionWithIndex = '{0}   {1}'.format(indexStr, question)

                if(not (question in questionsList)) or (repeat == 9):
                    questionsList.append(question)
                    questionsWithIndexList.append(questionWithIndex)
                    break

        drawPage(canvas, pageWidth, pageHeight, 30, 40, 40, fontSize, 0.8, questionsWithIndexList)

        if((repeatTimes > 1) and (repeatIndex < (repeatTimes - 1))):
            canvas.showPage()

    canvas.save()



