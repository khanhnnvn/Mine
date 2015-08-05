 @RequestMapping(value={"/accounts/sendMail"}, method={org.springframework.web.bind.annotation.RequestMethod.POST}, produces={"application/json"})
  @ResponseBody
  public Object resetPassword(@RequestParam(value="email", required=true) String email, @RequestParam(value="password", required=true) String password)
  {
    logger.info("called resetPassword {}", email);
    try
    {
      this.service.sendPasswordMail(email, password);
      return PostResultObj.getSuccessResult("OK");
    }
    catch (Exception e)
    {
      e.printStackTrace();
      logger.info(e.toString());
    }
    return new ResponseEntity(HttpStatus.INTERNAL_SERVER_ERROR);
  }


 public void sendMail(String from, String to, String subject, String msg)
  {
    SimpleMailMessage message = new SimpleMailMessage();
    
    message.setFrom(from);
    message.setTo(to);
    message.setSubject(subject);
    message.setText(msg);
    this.mailSender.send(message);
  }
  
  public void sendPasswordMail(String to, String newPass)
  {
    String body = "Your new password is\n" + newPass + "\n\nthis password is available while 30 minutes.";
    
    SimpleMailMessage mailMessage = new SimpleMailMessage(this.passwordResetMessage);
    mailMessage.setTo(to);
    mailMessage.setText(body);
    this.mailSender.send(mailMessage);
  }