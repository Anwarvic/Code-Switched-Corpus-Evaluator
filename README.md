# Code-Switched-Corpus-Evaluator
A python implementation of the "Comparing the Level of Code-Switching in Corpora" paper. This model is just an evaluator to evaluate the complexity score of a code-switched corpus.


## Benchmark

The following table is the complexity score of different code-switched dataset
provided by the LinCE benchmark:

<table>
    <thead>
        <tr>
            <th>Language Pair</th>
            <th>Download</th>
            <th>Filename</th>
            <th>Tokens</th>
            <th>Utterances</th>
            <th>Switched Utterances</th>
            <th>Score</th>
            <th>Paper</th>
        </tr>
    </thead>
    <tbody>
        <!-- First Entry -->
        <tr>
            <td rowspan=2>Spanish-English</td>
            <td rowspan=2><a href="https://ritual.uh.edu/lince/benchmark/lid_spaeng.zip">Link</a></td>
            <td>train.conll</td>
            <td>248363</td>
            <td>21014</td>
            <td>7236 (34.43%)</td>
            <td>84.68</td>
            <td rowspan=2><a href="https://aclanthology.org/W16-5805.pdf">Link</a></td>
        </tr>
        <tr>
            <td>dev.conll</td>
            <td>40058</td>
            <td>3328</td>
            <td>1101 (33.08%)</td>
            <td>79.54</td>
        </tr>
        <!-- Second Entry -->
        <tr>
            <td rowspan=2>Hindu-English</td>
            <td rowspan=2><a href="https://ritual.uh.edu/lince/benchmark/lid_hineng.zip">Link</a></td>
            <td>train.conll</td>
            <td>94389</td>
            <td>4823</td>
            <td>2095 (43.43%)</td>
            <td>96.44</td>
            <td rowspan=2><a href="https://www.aclweb.org/anthology/W18-3206.pdf">Link</a></td>
        </tr>
        <tr>
            <td>dev.conll</td>
            <td>15329</td>
            <td>744</td>
            <td>319 (42.87%)</td>
            <td>96.24</td>
        </tr>
        <!-- Third Entry -->
        <tr>
            <td rowspan=2>Hindu-English</td>
            <td rowspan=2><a href="https://ritual.uh.edu/lince/benchmark/lid_nepeng.zip">Link</a></td>
            <td>train.conll</td>
            <td>121918</td>
            <td>8451</td>
            <td>6479 (76.67%)</td>
            <td>113.17</td>
            <td rowspan=2><a href="https://www.aclweb.org/anthology/W14-3907.pdf">Link</a></td>
        </tr>
        <tr>
            <td>dev.conll</td>
            <td>19071</td>
            <td>1332</td>
            <td>923 (69.29%)</td>
            <td>109.78</td>
        </tr>
    </tbody>
</table>