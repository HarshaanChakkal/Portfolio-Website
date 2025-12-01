import {
  Mail,
  MapPin,
  Phone,
  Send

}
from "lucide-react";
import { cn } from "@/lib/utils";
import { useToast } from "@/hooks/use-toast";
import { useState } from "react";

export const ContactSection = () => {
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    const formData = new FormData();
    formData.append("name", e.target.name.value);
    formData.append("email", e.target.email.value);
    formData.append("message", e.target.message.value);

    try {
      const res = await fetch("https://portfolio-website-t4go.onrender.com/contact", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      console.log("Response:", data);

      if (res.ok) {
        toast({
          title: "Message sent!",
          description: "Your message has been delivered successfully.",
        });
        e.target.reset();
      } else {
        toast({
          title: "Error",
          description: data.error || "Failed to send message.",
        });
      }
    } catch (error) {
      console.error("Network error:", error);
      toast({
        title: "Error",
        description: "Something went wrong. Please try again later.",
      });
    } finally {
      setIsSubmitting(false);
    }
};

  return (
    // define the contact section structure
    <section id="contact" className="py-24 px-4 relative bg-secondary/30">
      <div className="container mx-auto max-w-5xl">
        <h2 className="text-3xl md:text-4xl font-bold mb-4 text-center">
         <span className="text-primary"> Contact Information</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          <div className="space-y-8">
            <h3 className="text-2xl font-semibold mb-6">

            </h3>

            <div className="space-y-6 justify-center">
              <div className="flex items-start space-x-4">
                <div className="p-3 rounded-full bg-primary/10">
                  <Mail className="h-6 w-6 text-primary" />{" "}
                </div>
                <div>
                  <h4 className="font-medium"> Email</h4>
                  <a
                    href="mailto:hello@gmail.com"
                    className="text-muted-foreground hover:text-primary transition-colors"
                  >
                    harshaanchakkal@gmail.com
                  </a>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="p-3 rounded-full bg-primary/10">
                  <Phone className="h-6 w-6 text-primary" />{" "}
                </div>
                <div>
                  <h4 className="font-medium"> Phone</h4>
                  <a
                    href="tel:+11234567890"
                    className="text-muted-foreground hover:text-primary transition-colors"
                  >
                    +1 (913) 638-3459
                  </a>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="p-3 rounded-full bg-primary/10">
                  <MapPin className="h-6 w-6 text-primary" />{" "}
                </div>
                <div>
                  <h4 className="font-medium"> Location</h4>
                  <a className="text-muted-foreground hover:text-primary transition-colors">
                    Olathe, Kansas
                  </a>
                </div>
              </div>
            </div>

            
          </div>

          <div className="bg-card p-8 rounded-lg shadow-xs">
  <h3 className="text-2xl font-semibold mb-6">Send a Message</h3>


  <form className="space-y-6" onSubmit={handleSubmit}>
    <div>
      <label htmlFor="name" className="block text-sm font-medium mb-2">
        Your Name
      </label>
      <input
        type="text"
        id="name"
        name="name"
        required
        className="w-full px-4 py-3 rounded-md border border-input bg-background"
      />
    </div>

    <div>
      <label htmlFor="email" className="block text-sm font-medium mb-2">
        Your Email
      </label>
      <input
        type="email"
        id="email"
        name="email"
        required
        className="w-full px-4 py-3 rounded-md border border-input bg-background"
      />
    </div>

    <div>
      <label htmlFor="message" className="block text-sm font-medium mb-2">
        Message
      </label>
      <textarea
        id="message"
        name="message"
        required
        className="w-full px-4 py-3 rounded-md border border-input bg-background resize-none"
      />
    </div>

    <button
      type="submit"
      disabled={isSubmitting}
      className={cn(
        "cosmic-button w-full flex items-center justify-center gap-2"
      )}
    >
      {isSubmitting ? "Sending..." : "Send Message"}
      <Send size={16} />
    </button>
  </form>
</div>

        </div>
      </div>
    </section>
  );
};
