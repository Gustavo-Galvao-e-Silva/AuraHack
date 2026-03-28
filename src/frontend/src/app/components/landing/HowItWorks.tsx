import { motion } from "motion/react";

const MotionDiv = motion.div;

export function HowItWorks() {
    return(
        <section className="px-4 sm:px-6 lg:px-8 py-20 bg-linear-to-b from-card/30 to-transparent">
        <div className="max-w-5xl mx-auto">
          <MotionDiv
            initial={{ y: 50, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl sm:text-5xl font-bold text-center mb-16 text-foreground">
              How It Works
            </h2>
          </MotionDiv>
          
          <div className="space-y-12">
            {[
              {
                step: "1",
                title: "Intelligent Vectorization",
                description: "Trial data and medical records are processed and vectorized using AI, enabling deep semantic analysis."
              },
              {
                step: "2",
                title: "Precise Matching",
                description: "Recommendation system based on relevance and compatibility, with match percentage for each patient-trial combination."
              },
              {
                step: "3",
                title: "Direct Connection",
                description: "Integrated messaging system allows secure and efficient communication between patients, doctors, and researchers."
              }
            ].map((step, i) => (
              <MotionDiv
                key={i}
                initial={{ x: i % 2 === 0 ? -100 : 100, opacity: 0 }}
                whileInView={{ x: 0, opacity: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: i * 0.2 }}
                className="flex flex-col md:flex-row gap-6 items-start"
              >
                <motion.div
                  className="w-16 h-16 rounded-2xl bg-linear-to-br from-primary to-secondary text-primary-foreground flex items-center justify-center text-2xl font-bold shrink-0 shadow-lg"
                  whileHover={{ scale: 1.1, rotate: 360 }}
                  transition={{ duration: 0.6 }}
                >
                  {step.step}
                </motion.div>
                <div className="flex-1">
                  <h3 className="text-2xl font-bold mb-2 text-foreground">{step.title}</h3>
                  <p className="text-muted-foreground text-lg">{step.description}</p>
                </div>
              </MotionDiv>
            ))}
          </div>
        </div>
      </section>
    );
}