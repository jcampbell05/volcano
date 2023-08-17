# Documentation

Volcano was made out of a frustration on the steep learning curve shell scripting can present,
to take one example "1=1" is not the same as "1 = 1" despite the fact that in modern programming
languages this would result in the same behaviour.

For many users they use shellscript primarily for it's portability, they are deploying in 
environments with limited space where they may not have access to any languages such as python.

Most attempts at solving this problem involve creating a new shell scripting syntax (Such as Oil and
Fish) which is removes the benefits of portability. Or a custom language which compiles into shell
but ends up abandoned since making a lanaguage from scratch is hard.

With Volcano we took a different approach. We took the robust foundation of python which has a battle tested syntax, mature modules for parsing it's syntax included and is one of the most
popular programming languages so presents a low barrier to entry. 

Since python typically comes as standard on almost all unix like  operating systems we have been
able to build a compiler that can be run almost anywhere with zero additional dependencies.

## Implementation

This is a living document and will be updated as we update Volcano, this is a brief guide to how
we've implemented various language features in shellscript.