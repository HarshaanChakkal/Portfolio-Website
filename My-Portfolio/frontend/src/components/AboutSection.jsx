import { Briefcase, Code, User } from "lucide-react";

// The AboutSection represents the about me section of the portfolio website.
export const AboutSection = () => {
  return (
    <section id="about" className="py-24 px-4 relative">
      <div className="container mx-auto max-w-5xl">
        <h2 className="text-5xl md:text-6xl font-bold mb-12 text-center">
          About <span className="text-primary"> Me</span>
        </h2>

        <div className="pt-4 opacity-0 animate-fade-in-delay-1">
          <div className="space-y-6">
            <h3 className="text-2xl font-semibold">
              Aspiring Software Engineer
            </h3>

            <p className="text-muted-foreground">
              I am an Honors Undergraduate Student at the University of Kansas majoring in Computer Science
              with a concentration in Economics and a Minor in Mathematics. I'm passionate about building 
              software that solves real-world problems, especially at the intersection of technology and finance.
            </p>

            <p className="text-muted-foreground">
              With experience in full-stack development, AI tools, and automation, I enjoy building data-driven 
              applications using a diverse set of modern technologies. My interdisciplinary background equips me 
              with both a problem-solving mindset and a creative approach to building efficient, user-focused solutions.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 pt-4 justify-center">
              <a href="#contact" className="cosmic-button">
                Get In Touch
              </a>

              {/* Insert your resume link in the href below */}
              <a
                href="/Harshaan-Resume copy.pdf"
                className="px-6 py-2 rounded-full border border-primary text-primary hover:bg-primary/10 transition-colors duration-300"
                target="_blank"
                rel="noopener noreferrer"
              >
                View Resume
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
