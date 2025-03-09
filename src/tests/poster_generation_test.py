from src.service.banner_service import generate_banner
from src.models.Profile import Profile



# Example Usage
if __name__ == "__main__":

    yaro_1 = Profile(name="John Se",
                    header = "Unity Developer | Software Engineer | Technical Game Designer",
                    picture = "../../assets/sample-image/yaro4.png",
                    pattern_bg = "../../assets/background-patterns/payam-pattern-bg-2.png")

    yaro_3 = Profile(name="Alvine Soladana",
                    header = "Backend Developer | Skilled in Next.js, Django, Express.js, Java, AWS | Master's in CS | Interested in CyberSecurity",
                    picture = "../../assets/sample-image/yaro-2.png",
                    pattern_bg = "../../assets/background-patterns/soroosh-pattern-bg.png")

    yaro_5 = Profile(name=" Petrouz Wozsi",
                    header = "MSc Chemist | Electrochemist | Computational Materials Scientist",
                    picture = "../../assets/sample-image/yaro-1.png",
                    pattern_bg = "../../assets/background-patterns/pezh-pattern-2.png")

    yaro_4 = Profile (name="Silva Angre",
                    header = "PhD Candidate | Computer Vision Researcher",
                    picture = "../../assets/sample-image/yaro-3.png",
                    pattern_bg = "../../assets/background-patterns/drvoid-pattern-bg.png")

    payam = Profile(name="Payam Ranjbar",
                    header = "Unity Developer | Software Engineer | Technical Game Designer",
                    picture = "../../assets/sample-image/payam.png",
                    pattern_bg = "../../assets/background-patterns/payam-pattern.png")

    generate_banner(payam)
    generate_banner(yaro_1)
    generate_banner(yaro_4)
    generate_banner(yaro_5)
    generate_banner(yaro_3)
