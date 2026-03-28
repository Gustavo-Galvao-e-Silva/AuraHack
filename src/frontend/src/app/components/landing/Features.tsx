import { motion } from "motion/react";
import { UserRound, Stethoscope, FlaskConical, CheckCircle2 } from "lucide-react";

const MotionDiv = motion.div;

export function Features() {
    return(
      <section className="px-4 sm:px-6 lg:px-8 py-20 bg-linear-to-b from-transparent to-card/30 relative">
        <div className="max-w-7xl mx-auto">
          <MotionDiv
            initial={{ y: 50, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl sm:text-5xl font-bold text-center mb-4 text-foreground">
              For Everyone in Clinical Research
            </h2>
            <p className="text-center text-muted-foreground text-lg mb-16 max-w-2xl mx-auto">
              Whether you're a patient seeking treatment, a doctor managing care, or a researcher conducting trials
            </p>
          </MotionDiv>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: UserRound,
                title: "Patients",
                description: "Find clinical trials compatible with your medical profile and access innovative treatments.",
                color: "primary",
                features: [
                  "Upload medical records",
                  "Automatic trial matching",
                  "Direct researcher connection"
                ]
              },
              {
                icon: Stethoscope,
                title: "Doctors",
                description: "Register patients and find treatment opportunities in relevant clinical trials.",
                color: "secondary",
                features: [
                  "Patient management",
                  "Intelligent recommendation system",
                  "Add and manage trials"
                ]
              },
              {
                icon: FlaskConical,
                title: "Researchers",
                description: "Publish your trials and find qualified patients efficiently.",
                color: "accent",
                features: [
                  "Trial management portal",
                  "Automatic patient matching",
                  "Integrated communication system"
                ]
              }
            ].map((card, i) => (
              <MotionDiv
                key={i}
                initial={{ y: 50, opacity: 0 }}
                whileInView={{ y: 0, opacity: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: i * 0.2 }}
                whileHover={{ y: -10, scale: 1.02 }}
              >
                <div className="bg-card rounded-2xl p-8 shadow-xl border border-border h-full backdrop-blur-sm hover:shadow-2xl transition-all duration-300 group relative overflow-hidden">
                  {/* Gradient overlay on hover */}
                  <div className="absolute inset-0 bg-linear-to-br from-primary/5 to-secondary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  
                  <div className="relative z-10">
                    <motion.div
                      className="w-16 h-16 rounded-2xl bg-linear-to-br from-primary/20 to-secondary/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300"
                      whileHover={{ rotate: [0, -10, 10, -10, 0] }}
                      transition={{ duration: 0.5 }}
                    >
                      <card.icon className="w-9 h-9 text-primary" />
                    </motion.div>
                    
                    <h3 className="text-2xl font-bold mb-4 text-foreground">{card.title}</h3>
                    <p className="text-muted-foreground mb-6">{card.description}</p>
                    
                    <ul className="space-y-3">
                      {card.features.map((feature, j) => (
                        <motion.li
                          key={j}
                          className="flex items-start gap-2"
                          initial={{ x: -20, opacity: 0 }}
                          whileInView={{ x: 0, opacity: 1 }}
                          viewport={{ once: true }}
                          transition={{ delay: i * 0.2 + j * 0.1 }}
                        >
                          <CheckCircle2 className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                          <span className="text-sm text-foreground">{feature}</span>
                        </motion.li>
                      ))}
                    </ul>
                  </div>
                </div>
              </MotionDiv>
            ))}
          </div>
        </div>
      </section>
    );
}