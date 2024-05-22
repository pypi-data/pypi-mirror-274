# ArtSnake

**Say no to art theft!** Robust and easy-to-use tool/API to protect digital art and photos from use without consent, combining context-aware watermarking and image poisoning.

## Current Scenario

Artists are often unable to protect their digital art from unauthorized use. No current solution combines the ease of use of traditional watermarking with the robustness of invisible watermarking and image poisoning techniques, and each has its own limitations.

Current watermark implementation tools are not context-aware. They can often be very easily removed by cropping or editing the image using modern image editing software and generative models, or obstruct the image in a way that is visually damaging to the art. 
**(For the prototype version of the project, this is the main concern)**

On the other side of the spectrum, current invisible watermarking techniques are often too complex for artists to use, and require a deep understanding of cryptography and image processing. And in the case of protection against generative models, they are often rely on the good faith of the model creators to respect the watermark, which does not provide a real solution to the problem. Anti-AI image poisoning techniques are, although powerful, not easily accessible in an easily integrable form for artists, especially those who do not possess computing resources or knowledge.

## References

### Papers

[On the Effectiveness of Visible Watermarks](https://openaccess.thecvf.com/content_cvpr_2017/papers/Dekel_On_the_Effectiveness_CVPR_2017_paper.pdf)

[Visible Watermark Detection in Images](https://cseweb.ucsd.edu//~sag043/static/pdfs/WatermarkDetection.pdf)

[An Adaptive Visible Watermark Embedding Method based on Region Selection](https://downloads.hindawi.com/journals/scn/2021/6693343.pdf?_gl=1*1z0ms72*_ga*ODYzNDMwNjk3LjE3MTU2ODQ3MDI.*_ga_NF5QFMJT5V*MTcxNTY4NDcwMi4xLjEuMTcxNTY4NTAzNC4yNC4wLjA.&_ga=2.191923690.1907549399.1715684710-863430697.1715684702)

[Adaptive Reversible Visible Watermarking Based on Total Variation for BTC-Compressed Images](https://cdn.techscience.cn/files/cmc/2023/TSP_CMC-74-3/TSP_CMC_34819/TSP_CMC_34819.pdf)

[Preventing Unauthorized AI Over-Analysis by Medical Image Adversarial Watermarking](https://arxiv.org/pdf/2303.09858)

[Benchmarking the Robustness of Image Watermarks](https://arxiv.org/pdf/2401.08573.pdf)

### Technologies of Interest
[ArtShield](https://artshield.io/)

[Glaze](https://glaze.cs.uchicago.edu/index.html)

[Sanative AI](https://app.sanative.ai/)

### Repositories of Interest

[umd-huang-lab/WAVES](https://github.com/umd-huang-lab/WAVES)

[rohitrango/automatic-watermark-detection](https://github.com/rohitrango/automatic-watermark-detection?tab=readme-ov-file)

[LAION-AI/watermark-detection](https://github.com/LAION-AI/watermark-detection)

[EspacioLatente/Glaze](https://github.com/EspacioLatente/Glaze)